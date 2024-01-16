from core.views import (
    AttendantViewSet,
    CustomerGroupViewSet,
    CustomerUpdateViewSet,
    CustomerViewSet,
    UserViewSet,
)
from rest_framework import routers

r = routers.DefaultRouter()
r.register("users", UserViewSet)
r.register("attendants", AttendantViewSet)
r.register("customers", CustomerViewSet)
r.register("updates", CustomerUpdateViewSet)
r.register("groups", CustomerGroupViewSet)

urlpatterns = r.urls
