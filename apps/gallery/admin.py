from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """Admin for gallery categories"""

    list_display = ('name', 'slug', 'order', 'image_count')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'order')
        }),
    )

    def image_count(self, obj):
        """Count of images in this category"""
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Admin for gallery images"""

    list_display = (
        'title',
        'image_preview',
        'category',
        'date_taken',
        'is_featured',
        'order',
        'uploaded_date'
    )
    list_filter = ('category', 'is_featured', 'date_taken', 'uploaded_date')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'caption')
    date_hierarchy = 'date_taken'
    ordering = ('-date_taken', '-uploaded_date')
    readonly_fields = ('uploaded_date',)

    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'category', 'image', 'caption')
        }),
        ('Date Information', {
            'fields': ('date_taken', 'uploaded_date')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
    )

    actions = ['mark_as_featured', 'unmark_as_featured']

    def image_preview(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 75px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'

    # Custom Actions
    @admin.action(description='Mark as featured')
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} image(s) marked as featured.')

    @admin.action(description='Unmark as featured')
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} image(s) unmarked as featured.')
