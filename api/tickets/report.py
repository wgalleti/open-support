from django.template.loader import render_to_string


class TicketReport:
    def __init__(self, ticket):
        self.ticket = ticket

    def get_html(self, template):
        context = dict(
            data=self.ticket, interacao=self.ticket.ticketinteracao_set.last()
        )
        return render_to_string(template, context)
