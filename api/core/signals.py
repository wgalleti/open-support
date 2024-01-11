from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cliente, Atendente, ClienteAtualizacao
from .services import UsuarioService
from .tasks import criar_usuario


def save_add_auth_user(instance):
    us = UsuarioService()
    us.link_user(instance)
    instance.usuario_acesso = us.user
    instance.save()
    return us


@receiver(post_save, sender=ClienteAtualizacao)
def save_atualizacao(sender, instance: ClienteAtualizacao, **kwargs):
    instance.cliente.versao = instance.versao
    instance.cliente.save()


@receiver(post_save, sender=Cliente)
def save_cliente(sender, instance: Cliente, **kwargs):
    post_save.disconnect(save_cliente, sender=sender)
    try:
        us = save_add_auth_user(instance)
        if us.created:
            criar_usuario.delay(us.user.id, us.new_password)
    except Exception as err:
        print('Falha ao sincronizar o usuario. Erro' + str(err))

    post_save.connect(save_cliente, sender=sender)


@receiver(post_save, sender=Atendente)
def save_atendente(sender, instance: Atendente, **kwargs):
    post_save.disconnect(save_atendente, sender=sender)
    try:
        us = save_add_auth_user(instance)
        if us.created:
            criar_usuario.delay(us.user.id, us.new_password)
    except Exception:
        print('Deu ruim')
    post_save.connect(save_atendente, sender=sender)
