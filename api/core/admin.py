from core.models import Attendant, CustomerGroup, MailError, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.register(MailError)

admin.site.site_header = "Base Support App"
admin.site.site_title = "Open Support"


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Custom info"), {"fields": ("foto", "is_atendente", "is_cliente", "nivel")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Attendant)
class AttendantAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    pass
