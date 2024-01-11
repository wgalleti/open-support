from rest_framework import routers

from core.views import AtendenteViewSet, ClienteViewSet, UserViewSet, ClienteAtualizacaoViewSet, GrupoClienteViewSet

r = routers.DefaultRouter()
r.register('users', UserViewSet)
r.register('atendentes', AtendenteViewSet)
r.register('clientes', ClienteViewSet)
r.register('clientesatualizacoes', ClienteAtualizacaoViewSet)
r.register('grupos', GrupoClienteViewSet)

urlpatterns = r.urls
