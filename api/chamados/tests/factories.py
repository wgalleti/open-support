import factory

from chamados.models import Ticket
from core.models import Cliente, Atendente


class AnexoFactory(factory.django.DjangoModelFactory):
    pass


class TicketFactory(factory.django.DjangoModelFactory):
    cliente = factory.Iterator(Cliente.objects.all())
    prioridade = factory.Iterator([i[0] for i in Ticket.PRIORIDADES])
    titulo = factory.Faker('company', locale='pt_BR')
    descricao = factory.Faker('text', locale='pt_BR')

    @factory.lazy_attribute
    def usuario_logado(self):
        return self.cliente.usuario_acesso

    class Meta:
        model = 'chamados.Ticket'


class TicketInteracaoFactory(factory.django.DjangoModelFactory):
    ticket = factory.Iterator(Ticket.objects.all())
    atendente = factory.Iterator(Atendente.objects.all())
    descricao = factory.Faker('text')
    interno = factory.Iterator([True, False])
    status = factory.Iterator([i[0] for i in Ticket.STATUS])
    departamento = factory.Iterator([i[0] for i in Ticket.DEPARTAMENTOS])

    @factory.lazy_attribute
    def usuario_logado(self):
        if not self.interno:
            return self.ticket.cliente.usuario_acesso

        return self.atendente.usuario_acesso

    class Meta:
        model = 'chamados.TicketInteracao'
