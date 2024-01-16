from django.contrib import admin

from .models import Ticket, TicketInteraction, Attachment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'logged_user',
        'customer',
        'started_at',
        'finished_at',
        'priority',
        'attendant',
        'title',
        'description',
        'status',
        'departament',
        'version',
        'level',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'logged_user',
        'customer',
        'started_at',
        'finished_at',
        'attendant',
    )
    raw_id_fields = ('files',)


@admin.register(TicketInteraction)
class TicketInteracaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'logged_user',
        'ticket',
        'date',
        'description',
        'is_internal',
        'status',
        'departament',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'logged_user',
        'ticket',
        'date',
        'attendant',
        'is_internal',
    )
    raw_id_fields = ('files',)


@admin.register(Attachment)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'date', 'user')

    list_filter = ('date', 'user')

    search_fields = ('user', 'file')
