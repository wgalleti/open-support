from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from core.helpers import choice_para_lista
from core.mixins import BaseViewSet
from .models import (
    TipoServico,
    Servico,
    OrdemServico,
    OrdemServicoItem,
    OrdemServicoTecnico,
)

from .serializers import (
    TipoServicoSerializer,
    ServicoSerializer,
    OrdemServicoSerializer,
    OrdemServicoItemSerializer,
    OrdemServicoTecnicoSerializer,
)
from .services import OrdemServicoService


class TipoServicoViewSet(BaseViewSet):
    serializer_class = TipoServicoSerializer
    queryset = TipoServico.objects.all()


class ServicoViewSet(BaseViewSet):
    serializer_class = ServicoSerializer
    queryset = Servico.objects.all()


class OrdemServicoViewSet(BaseViewSet):
    serializer_class = OrdemServicoSerializer
    queryset = OrdemServico.objects.all()

    @action(methods=['post'], detail=True)
    def cancelar(self, request, pk=None):
        os = self.get_object()
        data = request.data
        data['usuario'] = self.request.user.id

        try:
            s = OrdemServicoService(os)
            s.cancelar(data)

            return Response(status=200, data="Ordem de Serviço Cancelada")
        except Exception as e:
            return Response(status=400, data=str(e))

    @action(methods=['post'], detail=True)
    def finalizar(self, request, pk=None):
        os = self.get_object()
        data = request.data

        try:
            s = OrdemServicoService(os)
            s.finalizar(data)

            return Response(status=200, data='Ordem de Serviço Finalizada')
        except Exception as e:
            return Response(status=400, data=str(e))

    @action(methods=['post'], detail=True)
    def preparar_finalizacao(self, request, pk=None):
        os = self.get_object()
        user = self.request.user
        try:
            s = OrdemServicoService(os)
            data = s.preparar_finalizacao(user)

            return Response(status=200, data=data)
        except Exception as e:
            return Response(status=400, data=str(e))

    @action(methods=['get'], detail=False, url_path='status')
    def status(self, request, pk=None):
        print(request)
        return Response(choice_para_lista(OrdemServico.STATUS))


class OrdemServicoItemViewSet(BaseViewSet):
    serializer_class = OrdemServicoItemSerializer
    queryset = OrdemServicoItem.objects.all()


class OrdemServicoTecnicoViewSet(BaseViewSet):
    serializer_class = OrdemServicoTecnicoSerializer
    queryset = OrdemServicoTecnico.objects.all()

    filter_fields = ('id', 'ordem_servico',)
