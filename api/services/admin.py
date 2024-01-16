from django.contrib import admin

from .models import (
    ServiceType,
    Service,
    ServiceOrder,
    ServiceOrderItem,
    ServiceOrderTech,
)


@admin.register(ServiceType)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'value',
    )


@admin.register(Service)
class ServicoAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'erp_code',
    )


@admin.register(ServiceOrder)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'status',
        'customer',
        'description',
        'observation',
        'discount',
    )


@admin.register(ServiceOrderItem)
class OrdemServicoItemAdmin(admin.ModelAdmin):
    list_display = (
        'service_order',
        'service',
        'value',
        'duration',
    )


@admin.register(ServiceOrderTech)
class OrdemServicoTecnicoAdmin(admin.ModelAdmin):
    list_display = (
        'service_order',
        'service_type',
        'tech',
        'duration',
        'value',
    )
