from rest_framework import routers
from .views import (
    TipoServicoViewSet,
    ServicoViewSet,
    OrdemServicoViewSet,
    OrdemServicoItemViewSet,
    OrdemServicoTecnicoViewSet,
)

r = routers.DefaultRouter()

r.register('tipos', TipoServicoViewSet)
r.register('servicos', ServicoViewSet)
r.register('ordens', OrdemServicoViewSet)
r.register('itens', OrdemServicoItemViewSet)
r.register('tecnicos', OrdemServicoTecnicoViewSet)

urlpatterns = r.urls
