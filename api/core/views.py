from rest_framework import response
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from core.helpers import choice_para_lista
from core.integrations import ClienteIntegracao
from core.mixins import BaseViewSet
from core.models import Atendente, Cliente, User, GrupoCliente
from core.serializers import AtendenteSerializer, ClienteSerializer, UserSerializer, ClienteAtualizacaoSerializer, \
    GrupoClienteSerializer
from dbbackup import utils
from dbbackup.db.base import get_connector

from django.http import HttpResponse
from django.utils.encoding import smart_str


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-pk')
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @action(methods=['get'], detail=False)
    def backup(self, request, pk=None):
        connector = get_connector('default')
        filename = connector.generate_filename()
        outputfile = connector.create_dump()
        compressed_file, filename = utils.compress_file(outputfile, filename)
        outputfile = compressed_file
        outputfile.seek(0)
        response = HttpResponse(
            outputfile.read(),
            content_type="application/x-gzip"
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response['X-Sendfile'] = smart_str(outputfile.read())
        return response

    @action(methods=['get'], detail=False)
    def niveis(self, request, pk=None):
        return response.Response(choice_para_lista(User.NIVEIS))


class AtendenteViewSet(BaseViewSet):
    serializer_class = AtendenteSerializer
    queryset = Atendente.objects.all().order_by('-pk')

    def get_queryset(self):
        qs = self.queryset

        lookup = self.request.query_params.get('lookup', None)
        if lookup is not None:
            qs = qs.filter(ativo=True)

        return qs


class ClienteViewSet(BaseViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all().order_by('-pk')

    search_fields = ('=id', 'nome',)

    ordering = ['nome']

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user

        lookup = self.request.query_params.get('lookup', None)
        if lookup is not None:
            qs = qs.filter(ativo=True)

        if user.is_cliente:
            qs = qs.filter(usuario_acesso=user)

        return qs

    @action(methods=['GET'], detail=False)
    def existe(self, request, pk=None):
        email = request.query_params.get('email', None)
        if email is None:
            return response.Response('')

        if len(Cliente.objects.filter(email=email)) > 0:
            raise ParseError('Cliente já existe', code=400)

        if len(User.objects.filter(email=email)) > 0:
            raise ParseError('Usuário com esse email já existe', code=400)

        return response.Response('')

    @action(methods=['POST'], detail=False)
    def integrar(self, request, pk=None):
        c = ClienteIntegracao()
        c.integrar()

        return response.Response('')


class ClienteAtualizacaoViewSet(BaseViewSet):
    serializer_class = ClienteAtualizacaoSerializer
    queryset = Cliente.objects.all().order_by('-pk')


class GrupoClienteViewSet(BaseViewSet):
    serializer_class = GrupoClienteSerializer
    queryset = GrupoCliente.objects.all()

    @action(methods=['POST'], detail=True)
    def remover(self, request, pk=None):
        obj: GrupoCliente = self.get_object()
        cliente = self.request.data.get('id', None)

        if cliente is None:
            return Response(status=400, data='Cliente é obrigatório')

        try:
            obj.clientes.filter(id=cliente).delete()
            return Response(status=200, data='Cliente removido')
        except Exception as e:
            return Response(status=400, data='Cliente é obrigatório')

    @action(methods=['POST'], detail=True)
    def adicionar(self, request, pk=None):
        obj: GrupoCliente = self.get_object()
        cliente = self.request.data.get('id', None)

        if cliente is None:
            return Response(status=400, data='Cliente é obrigatório')

        try:
            obj.clientes.add(cliente)
            obj.save()
            return Response(status=200, data='Cliente adicionado')
        except Exception as e:
            return Response(status=400, data='Cliente é obrigatório')
