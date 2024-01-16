from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerUpdate
from .services import UsuarioService


def save_add_auth_user(instance):
    us = UsuarioService()
    us.link_user(instance)
    instance.usuario_acesso = us.user
    instance.save()
    return us


@receiver(post_save, sender=CustomerUpdate)
def save_atualizacao(sender, instance: CustomerUpdate, **kwargs):
    instance.customer.version = instance.version
    instance.customer.save()
