from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from chamados.models import Anexo, Ticket, TicketInteracao
from chamados.serializers import AnexoSerializer, TicketSerializer, TicketInteracaoSerializer, TicketDetalheSerializer
from chamados.services import TicketDashboardService, TicketService, TicketRapidoService
from core.helpers import choice_para_lista
from core.mixins import BaseViewSet
from servicos.serializers import OrdemServicoSerializer


class AnexoViewSet(BaseViewSet):
    serializer_class = AnexoSerializer
    queryset = Anexo.objects.all().order_by('-pk')
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (AllowAny,)


class TicketViewSet(BaseViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all().order_by('pk')
    filter_fields = ('id', 'status', 'prioridade', 'departamento',)

    def get_queryset(self):
        qs = self.queryset

        if self.request.query_params.get('all', None) is not None:
            return qs

        de = self.request.query_params.get('de')
        ate = self.request.query_params.get('ate')

        if de is not None:
            qs = qs.filter(inicio__gte=de)

        if ate is not None:
            qs = qs.filter(inicio__lte=ate)

        excludes = ['sem_atendimento']
        custom_filters = dict(
            finalizados=Q(status__in=[Ticket.FINALIZADO]),
            sem_atendimento=Q(id__in=TicketInteracao.objects.all().values_list('ticket', flat=True))
        )
        custom_filter = self.request.query_params.get('personalizado', None)

        if custom_filter is not None:
            try:
                filter = custom_filters[custom_filter]
            except:
                qs = qs
            else:
                if custom_filter in excludes:
                    qs = qs.exclude(filter)
                else:
                    qs = qs.filter(filter)

        if self.request.user.is_cliente:
            qs = qs.filter(cliente__usuario_acesso=self.request.user)

            if custom_filter is None:
                qs = qs.exclude(status__in=[Ticket.FINALIZADO])

        if self.request.user.is_atendente:
            qs = qs.filter(Q(atendente__usuario_acesso=self.request.user) | Q(nivel__lte=self.request.user.nivel))

            if custom_filter is None:
                qs = qs.exclude(status__in=[Ticket.FINALIZADO])

        if self.request.user.is_superuser:
            qs = qs.order_by('pk')

        return qs

    @action(methods=['post'], detail=False)
    def rapido(self, request, pk=None):
        try:
            data, user = request.data, request.user
            s = TicketRapidoService(data, user)
            data = s.registrar()
            return Response(status=200, data=data)
        except Exception as e:
            return Response(status=400, data=str(e))

    @action(methods=['get'], detail=False)
    def dashboard(self, requests, pk=None):
        ds = TicketDashboardService()
        response = dict(
            status=ds.get_status(),
            totais=ds.get_totais(),
            totais_clientes=ds.get_totais_cliente(),
            totais_atendente=ds.get_totais_atendente()
        )
        return Response(response)

    @action(methods=['get'], detail=True)
    def detalhes(self, requests, pk=None):
        self.queryset = Ticket.objects.all()

        t = self.get_object()
        return Response(TicketDetalheSerializer(t).data)

    @action(methods=['get'], detail=False)
    def prioridades(self, requests, pk=None):
        return Response(choice_para_lista(Ticket.PRIORIDADES))

    @action(methods=['get'], detail=False)
    def status(self, requests, pk=None):
        return Response(choice_para_lista(Ticket.STATUS))

    @action(methods=['get'], detail=False)
    def departamentos(self, requests, pk=None):
        return Response(choice_para_lista(Ticket.DEPARTAMENTOS))

    @action(methods=['post'], detail=True)
    def upgrade(self, request, pk=None):
        obj = self.get_object()
        try:
            s = TicketService(obj)
            t = s.upgrade(self.request.user)
            return Response(status=200, data=TicketSerializer(t).data)
        except Exception as e:
            return Response(status=400, data=str(e))

    @action(methods=['post'], detail=True)
    def gerar_os(self, request, pk=None):
        try:
            obj = self.get_object()
            s = TicketService(obj)
            os = s.gerar_os(self.request.user)
            return Response(OrdemServicoSerializer(os).data)
        except Exception as e:
            return Response(status=400, data=str(e))


class TicketInteracaoViewSet(BaseViewSet):
    serializer_class = TicketInteracaoSerializer
    queryset = TicketInteracao.objects.all().order_by('pk')
