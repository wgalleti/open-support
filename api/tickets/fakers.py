from core.models import Cliente, Atendente
from core.tests.factories import AtendenteFactory, ClienteFactory
from tickets.tests.factories import TicketFactory, TicketInteracaoFactory

from core.services import UsuarioService


def save_add_auth_user(instance):
    us = UsuarioService()
    us.link_user(instance)
    instance.usuario_acesso = us.user
    instance.save()
    return us


def processa_clientes():
    for c in Cliente.objects.all():
        us = save_add_auth_user(c)


def processa_atendentes():
    for a in Atendente.objects.all():
        us = save_add_auth_user(a)


ClienteFactory.create_batch(7)
AtendenteFactory.create_batch(5)

processa_clientes()
processa_atendentes()

for u in User.objects.all():
    u.set_password('123')
    u.save()

TicketFactory.create_batch(20)
TicketInteracaoFactory.create_batch(70)
