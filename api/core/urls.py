from rest_framework import routers

from core.views import AttendantViewSet, CustomerViewSet, UserViewSet, CustomerGroupViewSet, CustomerUpdateViewSet

r = routers.DefaultRouter()
r.register('users', UserViewSet)
r.register('attendants', AttendantViewSet)
r.register('customers', CustomerViewSet)
r.register('updates', CustomerUpdateViewSet)
r.register('groups', CustomerGroupViewSet)

urlpatterns = r.urls
