from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from rest_framework import serializers, viewsets


class TempoMixin(models.Model):
    """
    Controle de tempos
    Adiciona colunas criado_em e atualizado_em
    """
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name=_('update at')
    )

    class Meta:
        abstract = True


class UsuarioMixin(models.Model):
    """
    Controle de Usuário logado
    Adiciona coluna usuario_logado
    """
    usuario_logado = models.ForeignKey(
        to=get_user_model(),
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='%(app_label)s_%(class)s_logged_user',
        verbose_name=_('user in logged')
    )

    class Meta:
        abstract = True


class AtivoMixin(models.Model):
    """
    Controle de registro ativo
    Adiciona coluna ativo
    """
    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        abstract = True


class UsuarioSerializerMixin(serializers.ModelSerializer):
    """
    Serializer com usuário logado
    """
    logged_user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class BaseViewSet(viewsets.ModelViewSet):
    """
    Visão padrão herança
    """
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        # Verifica se quer listar todos os dados
        if bool(self.request.query_params.get('all', False)):
            self.pagination_class = None

        return super().list(request, *args, **kwargs)
