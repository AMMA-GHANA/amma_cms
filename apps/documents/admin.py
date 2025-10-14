from django.contrib import admin
from django.utils.html import format_html
from .models import DocumentCategory, Document


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    """Admin for document categories"""

    list_display = ('name', 'icon_display', 'slug', 'order', 'document_count')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'icon', 'order')
        }),
    )

    def icon_display(self, obj):
        """Display icon name"""
        return format_html(
            '<span style="font-family: monospace; background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">{}</span>',
            obj.icon
        )
    icon_display.short_description = 'Icon'

    def document_count(self, obj):
        """Count of documents in this category"""
        return obj.documents.count()
    document_count.short_description = 'Documents'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin for downloadable documents"""

    list_display = (
        'title',
        'thumbnail_preview',
        'category',
        'file_type_badge',
        'file_size',
        'download_count',
        'is_public',
        'is_featured',
        'uploaded_date'
    )
    list_filter = ('category', 'is_public', 'is_featured', 'uploaded_date', 'file_type')
    list_editable = ('is_public', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'uploaded_date'
    ordering = ('-uploaded_date',)
    readonly_fields = ('file_size', 'file_type', 'download_count', 'uploaded_date', 'updated_date')

    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('File', {
            'fields': ('file', 'thumbnail')
        }),
        ('File Information', {
            'fields': ('file_size', 'file_type', 'download_count'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_public', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('uploaded_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_public', 'mark_as_private', 'mark_as_featured', 'unmark_as_featured']

    def thumbnail_preview(self, obj):
        """Display thumbnail preview if available"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 60px; height: 80px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.thumbnail.url
            )
        return '-'
    thumbnail_preview.short_description = 'Preview'

    def file_type_badge(self, obj):
        """Display file type badge"""
        colors = {
            'PDF': '#dc3545',
            'DOC': '#007bff',
            'DOCX': '#007bff',
            'XLS': '#28a745',
            'XLSX': '#28a745'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.file_type, '#6c757d'),
            obj.file_type
        )
    file_type_badge.short_description = 'Type'

    # Custom Actions
    @admin.action(description='Mark as public')
    def mark_as_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} document(s) marked as public.')

    @admin.action(description='Mark as private')
    def mark_as_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} document(s) marked as private.')

    @admin.action(description='Mark as featured')
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} document(s) marked as featured.')

    @admin.action(description='Unmark as featured')
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} document(s) unmarked as featured.')
