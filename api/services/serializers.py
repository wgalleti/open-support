from rest_framework import serializers

from .models import (
    Service,
    ServiceOrder,
    ServiceOrderItem,
    ServiceOrderTech,
    ServiceType,
)


class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = "__all__"


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class OrdemServicoSerializer(serializers.ModelSerializer):
    valor = serializers.SerializerMethodField("_valor")
    valor_previsto = serializers.SerializerMethodField("_valor_previsto")

    def _valor(self, data):
        return data.value

    def _valor_previsto(self, data):
        return data.provided_value

    class Meta:
        model = ServiceOrder
        fields = "__all__"


class OrdemServicoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrderItem
        fields = "__all__"


class OrdemServicoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrderTech
        fields = "__all__"
