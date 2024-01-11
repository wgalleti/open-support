from rest_framework import serializers
from django.utils import timezone

from chamados.models import Anexo, Ticket, TicketInteracao
from core.models import Atendente


class AnexoSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField('_nome')

    def _nome(self, data: Anexo):
        return str(data.arquivo).split('/')[-1]

    class Meta:
        model = Anexo
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    usuario_logado = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cliente_display = serializers.SerializerMethodField('_cliente')
    data_display = serializers.SerializerMethodField('_data_display')
    anexos_display = serializers.SerializerMethodField('_anexos_display')
    aberto_cliente = serializers.SerializerMethodField('_aberto_cliente')
    usuario_display = serializers.SerializerMethodField('_usuario_display')
    telefone_cliente = serializers.SerializerMethodField('_contato_telefone_cliente')
    atendente_display = serializers.SerializerMethodField('_atendente_display')
    status_display = serializers.SerializerMethodField('_status_display')
    departamento_display = serializers.SerializerMethodField('_departamento_display')
    nivel_display = serializers.SerializerMethodField('_nivel_display')

    def _nivel_display(self, data: Ticket):
        return data.get_nivel_display()

    def _departamento_display(self, data: Ticket):
        return data.get_departamento_display()

    def _status_display(self, data: Ticket):
        return data.get_status_display()

    def _atendente_display(self, data: Ticket):
        return data.atendente.nome if data.atendente is not None else None;

    def _usuario_display(self, data: Ticket):
        if data.usuario_logado.is_atendente:
            return Atendente.objects.get(usuario_acesso=data.usuario_logado).nome
        return data.usuario_logado.username

    def _aberto_cliente(self, data: Ticket):
        return data.cliente.usuario_acesso == data.usuario_logado

    def _anexos_display(self, data: TicketInteracao):
        return AnexoSerializer(data.arquivos, many=True).data

    def _data_display(self, data: Ticket):
        return timezone.localtime(data.inicio).strftime("%d/%m/%Y %H:%M")

    def _cliente(self, data: Ticket):
        grupo = data.cliente.grupocliente_set.all().first()
        if grupo is None:
            return data.cliente.nome.title()

        return grupo.nome

    def _contato_telefone_cliente(self, data: Ticket):
        return data.cliente.contato_telefone

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketInteracaoSerializer(serializers.ModelSerializer):
    usuario_logado = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status_display = serializers.SerializerMethodField('_status')
    departamento_display = serializers.SerializerMethodField('_departamento')
    usuario_display = serializers.SerializerMethodField('_usuario')
    cliente_atendente = serializers.SerializerMethodField('_cliente_atendente')
    data_display = serializers.SerializerMethodField('_data_display')
    anexos_display = serializers.SerializerMethodField('_anexos_display')

    def _anexos_display(self, data: TicketInteracao):
        return AnexoSerializer(data.arquivos, many=True).data

    def _data_display(self, data: TicketInteracao):
        return timezone.localtime(data.data).strftime("%d/%m/%Y %H:%M")

    def _cliente_atendente(self, data: TicketInteracao):
        if data.usuario_logado is None:
            return 'atendente'

        return 'cliente' if data.usuario_logado.is_cliente else 'atendente'

    def _usuario(self, data: TicketInteracao):
        if data.usuario_logado.is_cliente:
            return data.ticket.cliente.nome
        elif data.usuario_logado.is_atendente:
            return Atendente.objects.get(usuario_acesso=data.usuario_logado_id).nome
        else:
            return data.usuario_logado.username

    def _departamento(self, data: TicketInteracao):
        return data.get_departamento_display()

    def _status(self, data: TicketInteracao):
        return data.get_status_display()

    class Meta:
        model = TicketInteracao
        fields = '__all__'


class TicketDetalheSerializer(TicketSerializer):
    andamentos = serializers.SerializerMethodField('_andamentos')
    cliente_display = serializers.SerializerMethodField('_cliente')

    def _cliente(self, data: Ticket):
        return data.cliente.nome

    def _andamentos(self, data: Ticket):
        return TicketInteracaoSerializer(data.ticketinteracao_set.all().order_by('data'), many=True).data

    class Meta:
        model = Ticket
        fields = '__all__'
