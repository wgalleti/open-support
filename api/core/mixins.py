from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from rest_framework import serializers, viewsets


class TimeModelMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('update at')
    )

    class Meta:
        abstract = True


class UserModelMixin(models.Model):
    logged_user = models.ForeignKey(
        to=get_user_model(),
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='%(app_label)s_%(class)s_logged_user',
        verbose_name=_('user in logged')
    )

    class Meta:
        abstract = True


class ActiveModelMixin(models.Model):
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        abstract = True


class UserSerializerMixin(serializers.ModelSerializer):
    logged_user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class BaseViewSet(viewsets.ModelViewSet):
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        if bool(self.request.query_params.get('all', False)):
            self.pagination_class = None

        return super().list(request, *args, **kwargs)
