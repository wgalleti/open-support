from django.contrib import admin

from .models import (
    TipoServico,
    Servico,
    OrdemServico,
    OrdemServicoItem,
    OrdemServicoTecnico,
)


@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'valor',
    )


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'codigo_erp',
    )


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'data',
        'status',
        'cliente',
        'descricao',
        'observacoes',
        'desconto',
    )


@admin.register(OrdemServicoItem)
class OrdemServicoItemAdmin(admin.ModelAdmin):
    list_display = (
        'ordem_servico',
        'servico',
        'valor',
        'tempo',
    )


@admin.register(OrdemServicoTecnico)
class OrdemServicoTecnicoAdmin(admin.ModelAdmin):
    list_display = (
        'ordem_servico',
        'tipo',
        'tecnico',
        'tempo',
        'valor',
    )
