from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Service, ServiceContentBlock


class ServiceContentBlockInline(admin.TabularInline):
    """Inline admin for service content blocks"""
    model = ServiceContentBlock
    extra = 1
    fields = ('block_type', 'title', 'content', 'data', 'order', 'is_active')
    ordering = ('order',)

    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for municipal services"""

    list_display = ('name', 'icon_display', 'has_detail_page', 'link_text', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'has_detail_page', 'created_at')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceContentBlockInline]

    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Detail Page Settings', {
            'fields': ('has_detail_page',),
            'description': 'Enable detail page to use content blocks below'
        }),
        ('Link Settings', {
            'fields': ('link_url', 'link_text'),
            'description': 'Leave link_url blank to use detail page, or provide external URL'
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


@admin.register(ServiceContentBlock)
class ServiceContentBlockAdmin(admin.ModelAdmin):
    """Admin for service content blocks"""
    list_display = ('__str__', 'service', 'block_type', 'title', 'order', 'is_active')
    list_filter = ('block_type', 'is_active', 'service')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'content', 'service__name')
    ordering = ('service', 'order')

    fieldsets = (
        ('Block Information', {
            'fields': ('service', 'block_type', 'title')
        }),
        ('Content', {
            'fields': ('content', 'data'),
            'description': 'Content supports markdown. Use data field for structured content like tables or service grids (JSON format)'
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
