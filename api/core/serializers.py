from dj_rest_auth.models import TokenModel
from rest_framework import serializers

from core.models import User, Customer, Attendant, CustomerUpdate, CustomerGroup


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField('_groups')
    permissions = serializers.SerializerMethodField('_permissions')
    customer = serializers.SerializerMethodField('_customer')

    def _customer(self, user: User):
        c = None
        if user.is_customer:
            c = Customer.objects.filter(usuario_acesso=user).first()
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


class AttendantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendant
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('_name')

    def _name(self, obj: Customer):
        return obj.name.title()

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUpdate
        fields = '__all__'


class CustomerGroupSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('_count')
    customers = CustomerSerializer(many=True, read_only=True)

    def _count(self, obj: CustomerGroup):
        return obj.count

    class Meta:
        model = CustomerGroup
        fields = '__all__'
