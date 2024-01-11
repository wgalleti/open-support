from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import TicketInteracao, Ticket
from .tasks import email_ticket


@receiver(post_save, sender=Ticket)
def save_ticket(sender, instance: Ticket, created, **kwargs):
    post_save.disconnect(save_ticket, sender=sender)

    if instance.status == Ticket.FINALIZADO:
        instance.termino = timezone.now()
        instance.save()

    post_save.connect(save_ticket, sender=sender)

    if created:
        email_ticket.delay(instance.id, f'Novo Ticket ({instance.id})')


@receiver(post_save, sender=TicketInteracao)
def save_interacao(sender, instance: TicketInteracao, **kwargs):
    if instance.atendente is not None:
        instance.ticket.atendente = instance.atendente

    if instance.status is not None:
        instance.ticket.status = instance.status

    if instance.departamento is not None:
        instance.ticket.departamento = instance.departamento

    instance.ticket.save()
    email_ticket.delay(instance.ticket.id, f'Nova Interação - Atendimento ({instance.ticket_id})', True)
