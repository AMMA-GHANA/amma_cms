from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectCategory, Project, ProjectImage


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """Admin for project categories"""

    list_display = ('name', 'icon_display', 'color_badge', 'slug', 'order', 'project_count')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color', 'order')
        }),
    )

    def icon_display(self, obj):
        """Display icon name"""
        return format_html(
            '<span style="font-family: monospace; background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">{}</span>',
            obj.icon
        )
    icon_display.short_description = 'Icon'

    def color_badge(self, obj):
        """Display color badge"""
        return format_html(
            '<span style="display: inline-block; width: 30px; height: 30px; background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></span>',
            obj.color
        )
    color_badge.short_description = 'Color'

    def project_count(self, obj):
        """Count of projects in this category"""
        return obj.projects.count()
    project_count.short_description = 'Projects'


class ProjectImageInline(admin.TabularInline):
    """Inline for project images"""
    model = ProjectImage
    extra = 1
    fields = ('image', 'image_preview', 'caption', 'is_primary', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 75px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for projects with inline images"""

    list_display = (
        'title',
        'primary_image_preview',
        'category',
        'status_badge',
        'location',
        'budget_display',
        'is_featured',
        'start_date'
    )
    list_filter = ('status', 'category', 'is_featured', 'start_date')
    list_editable = ('is_featured',)
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    ordering = ('-is_featured', 'order', '-start_date')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProjectImageInline]

    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'detailed_description')
        }),
        ('Classification', {
            'fields': ('category', 'status')
        }),
        ('Location and Timeline', {
            'fields': ('location', 'start_date', 'completion_date')
        }),
        ('Financial', {
            'fields': ('budget',)
        }),
        ('Impact Metrics', {
            'fields': ('beneficiaries', 'impact_icon', 'impact_text'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_featured', 'unmark_as_featured', 'mark_as_ongoing', 'mark_as_completed']

    def primary_image_preview(self, obj):
        """Display primary project image"""
        primary = obj.primary_image
        if primary:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                primary.image.url
            )
        return '-'
    primary_image_preview.short_description = 'Image'

    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'planned': '#007bff',
            'ongoing': '#fd7e14',
            'completed': '#28a745',
            'suspended': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def budget_display(self, obj):
        """Format budget display"""
        if obj.budget:
            return f"GHS {obj.budget:,.2f}"
        return '-'
    budget_display.short_description = 'Budget'

    # Custom Actions
    @admin.action(description='Mark as featured')
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} project(s) marked as featured.')

    @admin.action(description='Unmark as featured')
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} project(s) unmarked as featured.')

    @admin.action(description='Mark as ongoing')
    def mark_as_ongoing(self, request, queryset):
        updated = queryset.update(status='ongoing')
        self.message_user(request, f'{updated} project(s) marked as ongoing.')

    @admin.action(description='Mark as completed')
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} project(s) marked as completed.')
