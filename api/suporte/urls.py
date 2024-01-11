from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from suporte import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Suporte API",
        default_version='v1',
        description="Api de Suporte empresa Hifuzion",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="administrativo@hifuzion.com.br"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('dj_rest_auth.urls')),
                  path('core/', include('core.urls')),
                  path('chamados/', include('chamados.urls')),
                  path('servicos/', include('servicos.urls')),
                  re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
