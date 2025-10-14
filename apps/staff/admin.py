from django.contrib import admin
from django.utils.html import format_html
from .models import Department, StaffMember


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin for departments"""

    list_display = ('name', 'slug', 'order', 'staff_count')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'order')
        }),
    )

    def staff_count(self, obj):
        """Count of staff members in this department"""
        return obj.staff_members.count()
    staff_count.short_description = 'Staff Members'


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    """Admin for staff members and leadership"""

    list_display = (
        'full_name',
        'photo_preview',
        'position',
        'position_type_badge',
        'department',
        'is_active',
        'joined_date'
    )
    list_filter = ('position_type', 'department', 'is_active', 'joined_date')
    list_editable = ('is_active',)
    search_fields = ('full_name', 'position', 'bio', 'email')
    ordering = ('position_type', 'display_order', 'full_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'position', 'department', 'position_type')
        }),
        ('Biography and Photo', {
            'fields': ('bio', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Employment Details', {
            'fields': ('joined_date',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_active', 'mark_as_inactive', 'set_as_leadership', 'set_as_management']

    def photo_preview(self, obj):
        """Display staff photo thumbnail"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid #ddd;" />',
                obj.photo.url
            )
        return '-'
    photo_preview.short_description = 'Photo'

    def position_type_badge(self, obj):
        """Display position type with color coding"""
        colors = {
            'leadership': '#dc3545',
            'management': '#fd7e14',
            'staff': '#28a745'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.position_type, '#6c757d'),
            obj.get_position_type_display()
        )
    position_type_badge.short_description = 'Type'

    # Custom Actions
    @admin.action(description='Mark as active')
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} staff member(s) marked as active.')

    @admin.action(description='Mark as inactive')
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} staff member(s) marked as inactive.')

    @admin.action(description='Set as leadership')
    def set_as_leadership(self, request, queryset):
        updated = queryset.update(position_type='leadership')
        self.message_user(request, f'{updated} staff member(s) set as leadership.')

    @admin.action(description='Set as management')
    def set_as_management(self, request, queryset):
        updated = queryset.update(position_type='management')
        self.message_user(request, f'{updated} staff member(s) set as management.')
