from rest_framework import routers

from tickets.views import AnexoViewSet, TicketViewSet, TicketInteracaoViewSet

r = routers.DefaultRouter()

r.register('anexos', AnexoViewSet)
r.register('tickets', TicketViewSet)
r.register('ticketsinteracoes', TicketInteracaoViewSet)

urlpatterns = r.urls
