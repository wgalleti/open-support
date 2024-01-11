from rest_auth.models import TokenModel
from rest_framework import serializers

from core.models import Atendente, Cliente, User, ClienteAtualizacao, GrupoCliente


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField('_groups')
    permissions = serializers.SerializerMethodField('_permissions')
    cliente = serializers.SerializerMethodField('_cliente')

    def _cliente(self, user: User):
        c = None
        if user.is_cliente:
            c = Cliente.objects.filter(usuario_acesso=user).first()
        return c if c is None else c.id

    def _groups(self, user: User):
        if hasattr(user, 'groups'):
            return [dict(id=g.id, name=g.name) for g in user.groups.all()]
        return []

    def _permissions(self, user: User):
        if hasattr(user, 'user_permissions'):
            return [dict(id=p.id, name=p.name) for p in user.user_permissions.all()]
        return []

    class Meta:
        model = User
        exclude = ('password', 'user_permissions')


class TokenSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('_user')
    token = serializers.SerializerMethodField('_token')

    def _token(self, token: TokenModel):
        return token.key

    def _user(self, token: TokenModel):
        return UserSerializer(token.user).data

    class Meta:
        model = TokenModel
        fields = ('token', 'user',)


class AtendenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendente
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):

    nome = serializers.SerializerMethodField('_nome')

    def _nome(self, obj: Cliente):
        return obj.nome.title()

    class Meta:
        model = Cliente
        fields = '__all__'


class ClienteAtualizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteAtualizacao
        fields = '__all__'


class GrupoClienteSerializer(serializers.ModelSerializer):
    quantidade = serializers.SerializerMethodField('_quantidade')
    clientes = ClienteSerializer(many=True, read_only=True)


    def _quantidade(self, obj: GrupoCliente):
        return obj.quantidade

    class Meta:
        model = GrupoCliente
        fields = '__all__'
