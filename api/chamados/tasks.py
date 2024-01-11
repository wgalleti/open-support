from celery import shared_task

from chamados.models import Ticket
from chamados.report import TicketReport
from core.emails import HifuzionMail


@shared_task
def email_ticket(pk, title='Novo Ticket', interacao=False):

    ticket = Ticket.objects.get(id=pk)
    report = TicketReport(ticket)
    to = [ticket.cliente.email, ticket.usuario_logado.email]

    if len(ticket.ticketinteracao_set.all()) > 0:
        if ticket.ticketinteracao_set.all().last().interno:
            to = ['suporte@hifuzion.com.br']

    template = 'ticket/novo.html' if not interacao else 'ticket/interacao.html'

    if hasattr(ticket, 'atendente') and ticket.atendente is not None:
        to.append(ticket.atendente.email)

    mail = HifuzionMail(title,
                        report.get_html(template),
                        to)
    mail.send()
