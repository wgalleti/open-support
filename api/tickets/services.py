import datetime
import re
from datetime import date

from core.models import Attendant, Customer, User
from django.db.models import (
    Case,
    CharField,
    Count,
    F,
    IntegerField,
    Q,
    Sum,
    Value,
    When,
)
from services.models import ServiceOrder
from tickets.models import Ticket, TicketInteraction
from tickets.serializers import TicketInteracaoSerializer, TicketSerializer


class TicketRapidoService:
    def __init__(self, data, user: User):
        atendente = Attendant.objects.filter(usuario_acesso=user).first()
        cliente = Customer.objects.filter(id=data.get("cliente")).first()

        self.ticket = Ticket(
            cliente=cliente,
            inicio=datetime.datetime.now(),
            atendente=atendente,
            titulo="Atendimento Rápido",
            descricao=data.get("descricao"),
            status=Ticket.WORKING,
            departamento=Ticket.SUPPORT,
            versao=data.get(
                "versao", cliente.clienteatualizacao_set.all().last().version
            ),
            nivel=data.get("nivel", User.LEVEL1),
            usuario_logado=user,
        )
        self.interacao = TicketInteraction(
            ticket=self.ticket,
            usuario_logado=user,
            atendente=atendente,
            data=datetime.datetime.now(),
            descricao=data.get("solucao"),
            interno=False,
            status=Ticket.DEPLOYED,
            departamento=Ticket.SUPPORT,
        )

    def registrar(self):
        self.ticket.save()
        self.interacao.save()

        return TicketSerializer(self.ticket).data


class TicketService:
    def __init__(self, obj: Ticket):
        self.obj = obj

    def upgrade(self, user: User):
        if self.obj.level < 3:
            self.obj.level += 1
            self.obj.save()

            TicketInteraction(
                ticket=self.obj,
                descricao=f"Direcionou o ticket para o nível {self.obj.level}",
                interno=True,
                usuario_logado=user,
            ).save()

        return self.obj

    def gerar_os(self, user: User):
        TAG_RE = re.compile(r"<[^>]+>")

        os = ServiceOrder(
            data=date.today(),
            status=ServiceOrder.STARTED,
            cliente=self.obj.customer,
            descricao=TAG_RE.sub("", self.obj.description),
            observacoes=f"OS gerada através do ticket {self.obj.pk} aberto em {self.obj.started_at}",
            desconto=0,
        )
        os.save()

        self.obj.service_order = os
        self.obj.save()

        TicketInteraction(
            ticket=self.obj,
            descricao=f"Gerou a OS {os.pk} para tratrar dos assuntos desse ticket",
            interno=True,
            usuario_logado=user,
        ).save()

        return os


class TicketDashboardService:
    def get_status(self):
        choices = dict(Ticket._meta.get_field("status").flatchoices)
        whens = [When(status=k, then=Value(v)) for k, v in choices.items()]

        return (
            Ticket.objects.all()
            .annotate(status_display=Case(*whens, output_field=CharField()))
            .values("status_display")
            .annotate(
                total_ticktes=Count("id", distinct=True),
                total_atendente=Count("atendente", distinct=True),
            )
        )

    def get_totais(self):
        return Ticket.objects.all().aggregate(
            total_ticktes=Count("id", distinct=True),
            sem_atendente=Count("id", filter=Q(atendente_id=None)),
            finalizados=Count("id", filter=Q(status=Ticket.DEPLOYED)),
            pendentes=Count("id", filter=Q(status=Ticket.STATED)),
            aguardando_cliente=Count("id", filter=Q(status=Ticket.MORE_INFORMATION)),
            prioridade=Count(
                "id", filter=~Q(status=Ticket.DEPLOYED) & Q(prioridade=Ticket.HIGH)
            ),
        )

    def get_totais_cliente(self):
        return (
            Ticket.objects.all()
            .values("cliente__nome")
            .annotate(
                cliente_nome=F("cliente__nome"),
                total_ticktes=Count("id", distinct=True),
                finalizados=Sum(
                    Case(
                        When(status=Ticket.DEPLOYED, then=1),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                aguardando_cliente=Sum(
                    Case(
                        When(status=Ticket.MORE_INFORMATION, then=1),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
            )
            .values(
                "cliente_nome", "total_ticktes", "finalizados", "aguardando_cliente"
            )
            .distinct()
        )

    def get_totais_atendente(self):
        return (
            Ticket.objects.all()
            .exclude(atendente=None)
            .values("atendente__nome")
            .annotate(
                atendente_nome=F("atendente__nome"),
                total_ticktes=Count("id", distinct=True),
                finalizados=Sum(
                    Case(
                        When(status=Ticket.DEPLOYED, then=1),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                aguardando_cliente=Sum(
                    Case(
                        When(status=Ticket.MORE_INFORMATION, then=1),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
            )
            .distinct()
            .values(
                "atendente_nome", "total_ticktes", "finalizados", "aguardando_cliente"
            )
        )
