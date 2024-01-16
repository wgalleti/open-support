from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from support import settings

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("auth/", include("dj_rest_auth.urls")),
        path("core/", include("core.urls")),
        path("chamados/", include("tickets.urls")),
        path("servicos/", include("services.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
