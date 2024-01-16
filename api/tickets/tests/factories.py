import factory

from tickets.models import Ticket
from core.models import Cliente, Atendente


class AnexoFactory(factory.django.DjangoModelFactory):
    pass


class TicketFactory(factory.django.DjangoModelFactory):
    cliente = factory.Iterator(Cliente.objects.all())
    prioridade = factory.Iterator([i[0] for i in Ticket.PRIORITIES])
    titulo = factory.Faker('company', locale='pt_BR')
    descricao = factory.Faker('text', locale='pt_BR')

    @factory.lazy_attribute
    def usuario_logado(self):
        return self.cliente.usuario_acesso

    class Meta:
        model = 'tickets.Ticket'


class TicketInteracaoFactory(factory.django.DjangoModelFactory):
    ticket = factory.Iterator(Ticket.objects.all())
    atendente = factory.Iterator(Atendente.objects.all())
    descricao = factory.Faker('text')
    interno = factory.Iterator([True, False])
    status = factory.Iterator([i[0] for i in Ticket.STATUS])
    departamento = factory.Iterator([i[0] for i in Ticket.DEPARTMENTS])

    @factory.lazy_attribute
    def usuario_logado(self):
        if not self.interno:
            return self.ticket.customer.usuario_acesso

        return self.atendente.usuario_acesso

    class Meta:
        model = 'tickets.TicketInteracao'
