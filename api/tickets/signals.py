from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import TicketInteraction, Ticket


@receiver(post_save, sender=Ticket)
def save_ticket(sender, instance: Ticket, created, **kwargs):
    post_save.disconnect(save_ticket, sender=sender)

    if instance.status == Ticket.DEPLOYED:
        instance.finished_at = timezone.now()
        instance.save()

    post_save.connect(save_ticket, sender=sender)

    # if created:
        # email_ticket.delay(instance.id, f'Novo Ticket ({instance.id})')


@receiver(post_save, sender=TicketInteraction)
def save_interacao(sender, instance: TicketInteraction, **kwargs):
    if instance.attendant is not None:
        instance.ticket.attendant = instance.attendant

    if instance.status is not None:
        instance.ticket.status = instance.status

    if instance.departament is not None:
        instance.ticket.departament = instance.departament

    instance.ticket.save()
    # email_ticket.delay(instance.ticket.id, f'Nova Interação - Atendimento ({instance.ticket_id})', True)
