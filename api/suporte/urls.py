from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from suporte import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('dj_rest_auth.urls')),
                  path('core/', include('core.urls')),
                  path('chamados/', include('chamados.urls')),
                  path('servicos/', include('servicos.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
