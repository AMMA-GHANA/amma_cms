from django.contrib import admin
from django.utils.html import format_html
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for municipal services"""

    list_display = ('name', 'icon_display', 'link_text', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Link Settings', {
            'fields': ('link_url', 'link_text')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_active', 'mark_as_inactive']

    def icon_display(self, obj):
        """Display icon name with styling"""
        return format_html(
            '<span style="font-family: monospace; background: #f0f0f0; padding: 2px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            obj.icon
        )
    icon_display.short_description = 'Icon'

    # Custom Actions
    @admin.action(description='Mark as active')
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} service(s) marked as active.')

    @admin.action(description='Mark as inactive')
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} service(s) marked as inactive.')
