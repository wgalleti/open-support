from django.contrib import admin

from .models import Ticket, TicketInteracao, Anexo


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'criado_em',
        'atualizado_em',
        'usuario_logado',
        'cliente',
        'inicio',
        'termino',
        'prioridade',
        'atendente',
        'titulo',
        'descricao',
        'status',
        'departamento',
        'versao',
        'nivel',
    )
    list_filter = (
        'criado_em',
        'atualizado_em',
        'usuario_logado',
        'cliente',
        'inicio',
        'termino',
        'atendente',
    )
    raw_id_fields = ('arquivos',)


@admin.register(TicketInteracao)
class TicketInteracaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'criado_em',
        'atualizado_em',
        'usuario_logado',
        'ticket',
        'data',
        'data',
        'descricao',
        'interno',
        'status',
        'departamento',
    )
    list_filter = (
        'criado_em',
        'atualizado_em',
        'usuario_logado',
        'ticket',
        'atendente',
        'data',
        'interno',
    )
    raw_id_fields = ('arquivos',)


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ('id', 'arquivo', 'data', 'usuario')

    list_filter = ('data', 'usuario')

    search_fields = ('usuario', 'arquivo')
