from rest_framework import response
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from core.helpers import choice_para_lista
from core.mixins import BaseViewSet
from core.models import User, Attendant, Customer, CustomerUpdate, CustomerGroup
from core.serializers import (
    AttendantSerializer,
    CustomerSerializer,
    UserSerializer,
    CustomerUpdateSerializer,
    CustomerGroupSerializer,
)


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-pk')
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @action(methods=['get'], detail=False)
    def niveis(self, request, pk=None):
        return response.Response(choice_para_lista(User.LEVELS))


class AttendantViewSet(BaseViewSet):
    serializer_class = AttendantSerializer
    queryset = Attendant.objects.all().order_by('-pk')

    def get_queryset(self):
        qs = self.queryset

        lookup = self.request.query_params.get('lookup', None)
        if lookup is not None:
            qs = qs.filter(ativo=True)

        return qs


class CustomerViewSet(BaseViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by('-pk')

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
    def exists(self, request, pk=None):
        email = request.query_params.get('email', None)
        if email is None:
            return response.Response('')

        if len(Customer.objects.filter(email=email)) > 0:
            raise ParseError('Cliente já existe', code=400)

        if len(User.objects.filter(email=email)) > 0:
            raise ParseError('Usuário com esse email já existe', code=400)

        return response.Response('')


class CustomerUpdateViewSet(BaseViewSet):
    serializer_class = CustomerUpdateSerializer
    queryset = CustomerUpdate.objects.all().order_by('-pk')


class CustomerGroupViewSet(BaseViewSet):
    serializer_class = CustomerGroupSerializer
    queryset = CustomerGroup.objects.all()

    @action(methods=['POST'], detail=True)
    def remove(self, request, pk=None):
        obj: CustomerGroup = self.get_object()
        cliente = self.request.date.get('id', None)

        if cliente is None:
            return Response(status=400, data='Customer is required')

        try:
            obj.customers.filter(id=cliente).delete()
            return Response(status=200, data='Customer removed')
        except Exception as e:
            return Response(status=400, data='Customer is required')

    @action(methods=['POST'], detail=True)
    def to_add(self, request, pk=None):
        obj: CustomerGroup = self.get_object()
        cliente = self.request.date.get('id', None)

        if cliente is None:
            return Response(status=400, data='Customer is required')

        try:
            obj.customers.add(cliente)
            obj.save()
            return Response(status=200, data='Customer to add')
        except Exception as e:
            return Response(status=400, data='Customer is required')
