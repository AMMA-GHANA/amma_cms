from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    """Admin for contact form submissions"""

    list_display = (
        'name',
        'email',
        'subject_badge',
        'read_status',
        'submitted_date',
        'message_preview'
    )
    list_filter = ('subject', 'is_read', 'submitted_date')
    search_fields = ('name', 'email', 'message', 'phone')
    date_hierarchy = 'submitted_date'
    ordering = ('-submitted_date',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'submitted_date')

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'submitted_date')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'description': 'Internal notes (not visible to submitter)'
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def has_add_permission(self, request):
        # Prevent manual creation of inquiries (they come from the website)
        return False

    def read_status(self, obj):
        """Display read status with icon"""
        if obj.is_read:
            return format_html(
                '<span style="color: #28a745;">✓ Read</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">✗ Unread</span>'
        )
    read_status.short_description = 'Status'

    def subject_badge(self, obj):
        """Display subject with color coding"""
        colors = {
            'general': '#007bff',
            'complaint': '#dc3545',
            'suggestion': '#28a745',
            'service': '#fd7e14',
            'other': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.subject, '#6c757d'),
            obj.get_subject_display()
        )
    subject_badge.short_description = 'Subject'

    def message_preview(self, obj):
        """Display truncated message preview"""
        max_length = 50
        if len(obj.message) > max_length:
            return f"{obj.message[:max_length]}..."
        return obj.message
    message_preview.short_description = 'Message Preview'

    # Custom Actions
    @admin.action(description='Mark as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} inquiry/inquiries marked as read.')

    @admin.action(description='Mark as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} inquiry/inquiries marked as unread.')

    def get_list_display_links(self, request, list_display):
        """Make name clickable to view details"""
        return ('name',)
