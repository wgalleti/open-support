from core.models import Attendant
from django.utils import timezone
from rest_framework import serializers
from tickets.models import Attachment, Ticket, TicketInteraction


class AnexoSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField("_nome")

    def _nome(self, data: Attachment):
        return str(data.file).split("/")[-1]

    class Meta:
        model = Attachment
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    usuario_logado = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cliente_display = serializers.SerializerMethodField("_cliente")
    data_display = serializers.SerializerMethodField("_data_display")
    anexos_display = serializers.SerializerMethodField("_anexos_display")
    aberto_cliente = serializers.SerializerMethodField("_aberto_cliente")
    usuario_display = serializers.SerializerMethodField("_usuario_display")
    telefone_cliente = serializers.SerializerMethodField("_contato_telefone_cliente")
    atendente_display = serializers.SerializerMethodField("_atendente_display")
    status_display = serializers.SerializerMethodField("_status_display")
    departamento_display = serializers.SerializerMethodField("_departamento_display")
    nivel_display = serializers.SerializerMethodField("_nivel_display")

    def _nivel_display(self, data: Ticket):
        return data.get_nivel_display()

    def _departamento_display(self, data: Ticket):
        return data.get_departamento_display()

    def _status_display(self, data: Ticket):
        return data.get_status_display()

    def _atendente_display(self, data: Ticket):
        return data.attendant.nome if data.attendant is not None else None

    def _usuario_display(self, data: Ticket):
        if data.logged_user.is_atendente:
            return Attendant.objects.get(usuario_acesso=data.logged_user).name
        return data.logged_user.username

    def _aberto_cliente(self, data: Ticket):
        return data.customer.usuario_acesso == data.logged_user

    def _anexos_display(self, data: TicketInteraction):
        return AnexoSerializer(data.files, many=True).data

    def _data_display(self, data: Ticket):
        return timezone.localtime(data.started_at).strftime("%d/%m/%Y %H:%M")

    def _cliente(self, data: Ticket):
        grupo = data.customer.grupocliente_set.all().first()
        if grupo is None:
            return data.customer.nome.title()

        return grupo.name

    def _contato_telefone_cliente(self, data: Ticket):
        return data.customer.contato_telefone

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketInteracaoSerializer(serializers.ModelSerializer):
    usuario_logado = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status_display = serializers.SerializerMethodField("_status")
    departamento_display = serializers.SerializerMethodField("_departamento")
    usuario_display = serializers.SerializerMethodField("_usuario")
    cliente_atendente = serializers.SerializerMethodField("_cliente_atendente")
    data_display = serializers.SerializerMethodField("_data_display")
    anexos_display = serializers.SerializerMethodField("_anexos_display")

    def _anexos_display(self, data: TicketInteraction):
        return AnexoSerializer(data.files, many=True).data

    def _data_display(self, data: TicketInteraction):
        return timezone.localtime(data.date).strftime("%d/%m/%Y %H:%M")

    def _cliente_atendente(self, data: TicketInteraction):
        if data.logged_user is None:
            return "atendente"

        return "cliente" if data.logged_user.is_cliente else "atendente"

    def _usuario(self, data: TicketInteraction):
        if data.logged_user.is_cliente:
            return data.ticket.customer.nome
        elif data.logged_user.is_atendente:
            return Attendant.objects.get(usuario_acesso=data.usuario_logado_id).name
        else:
            return data.logged_user.username

    def _departamento(self, data: TicketInteraction):
        return data.get_departamento_display()

    def _status(self, data: TicketInteraction):
        return data.get_status_display()

    class Meta:
        model = TicketInteraction
        fields = "__all__"


class TicketDetalheSerializer(TicketSerializer):
    andamentos = serializers.SerializerMethodField("_andamentos")
    cliente_display = serializers.SerializerMethodField("_cliente")

    def _cliente(self, data: Ticket):
        return data.customer.nome

    def _andamentos(self, data: Ticket):
        return TicketInteracaoSerializer(
            data.ticketinteracao_set.all().order_by("data"), many=True
        ).data

    class Meta:
        model = Ticket
        fields = "__all__"
