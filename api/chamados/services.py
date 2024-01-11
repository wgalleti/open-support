import datetime
import re
from datetime import date

from django.db.models import F, Count, Sum, IntegerField, Q, Case, Value, When, CharField

from chamados.models import Ticket, TicketInteracao
from chamados.serializers import TicketSerializer, TicketInteracaoSerializer
from core.models import User, Atendente, Cliente
from servicos.models import OrdemServico


class TicketRapidoService:

    def __init__(self, data, user: User):

        atendente = Atendente.objects.filter(usuario_acesso=user).first()
        cliente = Cliente.objects.filter(id=data.get('cliente')).first()

        self.ticket = Ticket(
            cliente=cliente,
            inicio=datetime.datetime.now(),
            atendente=atendente,
            titulo='Atendimento Rápido',
            descricao=data.get('descricao'),
            status=Ticket.ESTAMOS_TRABALHANDO,
            departamento=Ticket.SUPORTE,
            versao=data.get('versao', cliente.clienteatualizacao_set.all().last().versao),
            nivel=data.get('nivel', User.NIVEL1),
            usuario_logado=user
        )
        self.interacao = TicketInteracao(
            ticket=self.ticket,
            usuario_logado=user,
            atendente=atendente,
            data=datetime.datetime.now(),
            descricao=data.get('solucao'),
            interno=False,
            status=Ticket.FINALIZADO,
            departamento=Ticket.SUPORTE,
        )

    def registrar(self):
        self.ticket.save()
        self.interacao.save()

        return TicketSerializer(self.ticket).data


class TicketService:
    def __init__(self, obj: Ticket):
        self.obj = obj

    def upgrade(self, user: User):
        if self.obj.nivel < 3:
            self.obj.nivel += 1
            self.obj.save()

            TicketInteracao(
                ticket=self.obj,
                descricao=f'Direcionou o ticket para o nível {self.obj.nivel}',
                interno=True,
                usuario_logado=user
            ).save()

        return self.obj

    def gerar_os(self, user: User):
        TAG_RE = re.compile(r'<[^>]+>')

        os = OrdemServico(
            data=date.today(),
            status=OrdemServico.INICIADA,
            cliente=self.obj.cliente,
            descricao=TAG_RE.sub('', self.obj.descricao),
            observacoes=f'OS gerada através do ticket {self.obj.pk} aberto em {self.obj.inicio}',
            desconto=0
        )
        os.save()

        self.obj.os = os
        self.obj.save()

        TicketInteracao(
            ticket=self.obj,
            descricao=f'Gerou a OS {os.pk} para tratrar dos assuntos desse ticket',
            interno=True,
            usuario_logado=user
        ).save()

        return os


class TicketDashboardService:

    def get_status(self):
        choices = dict(Ticket._meta.get_field('status').flatchoices)
        whens = [When(status=k, then=Value(v)) for k, v in choices.items()]

        return (
            Ticket
            .objects
            .all()
            .annotate(status_display=Case(*whens, output_field=CharField()))
            .values('status_display')
            .annotate(
                total_ticktes=Count('id', distinct=True),
                total_atendente=Count('atendente', distinct=True)
            )
        )

    def get_totais(self):
        return (
            Ticket.objects.all()
            .aggregate(
                total_ticktes=Count('id', distinct=True),
                sem_atendente=Count('id', filter=Q(atendente_id=None)),
                finalizados=Count('id', filter=Q(status=Ticket.FINALIZADO)),
                pendentes=Count('id', filter=Q(status=Ticket.INICIADO)),
                aguardando_cliente=Count('id', filter=Q(status=Ticket.PRECISAMOS_INFORMACOES)),
                prioridade=Count('id', filter=~Q(status=Ticket.FINALIZADO) & Q(prioridade=Ticket.ALTA)),
            )
        )

    def get_totais_cliente(self):
        return (Ticket.objects.all()
                .values('cliente__nome')
                .annotate(
            cliente_nome=F('cliente__nome'),
            total_ticktes=Count('id', distinct=True),
            finalizados=Sum(Case(
                When(status=Ticket.FINALIZADO, then=1),
                default=0,
                output_field=IntegerField(),
            )),
            aguardando_cliente=Sum(Case(
                When(status=Ticket.PRECISAMOS_INFORMACOES, then=1),
                default=0,
                output_field=IntegerField(),
            )),
        ).values('cliente_nome', 'total_ticktes', 'finalizados', 'aguardando_cliente').distinct())

    def get_totais_atendente(self):
        return (Ticket.objects.all().exclude(atendente=None)
                .values('atendente__nome')
                .annotate(
            atendente_nome=F('atendente__nome'),
            total_ticktes=Count('id', distinct=True),
            finalizados=Sum(Case(
                When(status=Ticket.FINALIZADO, then=1),
                default=0,
                output_field=IntegerField(),
            )),
            aguardando_cliente=Sum(Case(
                When(status=Ticket.PRECISAMOS_INFORMACOES, then=1),
                default=0,
                output_field=IntegerField(),
            )),
        ).distinct().values('atendente_nome', 'total_ticktes', 'finalizados', 'aguardando_cliente'))
