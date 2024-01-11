from rest_framework import serializers
from .models import (
    TipoServico,
    Servico,
    OrdemServico,
    OrdemServicoItem,
    OrdemServicoTecnico,
)


class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = '__all__'


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'


class OrdemServicoSerializer(serializers.ModelSerializer):
    valor = serializers.SerializerMethodField('_valor')
    valor_previsto = serializers.SerializerMethodField('_valor_previsto')

    def _valor(self, data):
        return data.valor

    def _valor_previsto(self, data):
        return data.valor_previsto

    class Meta:
        model = OrdemServico
        fields = '__all__'


class OrdemServicoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServicoItem
        fields = '__all__'


class OrdemServicoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServicoTecnico
        fields = '__all__'
