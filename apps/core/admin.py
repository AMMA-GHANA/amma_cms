from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, HeroSlide, Statistic, AboutSection


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for site-wide settings (singleton)"""

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of site settings
        return False

    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline')
        }),
        ('Logos and Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'office_hours')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
    )

    def changelist_view(self, request, extra_context=None):
        # Redirect to the single instance edit page
        obj = SiteSettings.load()
        return self.changeform_view(request, str(obj.pk), extra_context=extra_context)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    """Admin for homepage hero carousel slides"""

    list_display = ('title', 'slide_preview', 'button_text', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle', 'button_text')
    ordering = ('order', '-created_at')

    fieldsets = (
        ('Slide Content', {
            'fields': ('title', 'subtitle', 'image')
        }),
        ('Call to Action', {
            'fields': ('button_text', 'button_link'),
            'description': 'Optional button for the slide'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def slide_preview(self, obj):
        """Display image thumbnail in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    slide_preview.short_description = 'Preview'


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """Admin for homepage statistics cards"""

    list_display = ('label', 'value', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('label', 'value')
    ordering = ('order',)

    fieldsets = (
        ('Statistic Details', {
            'fields': ('label', 'value', 'icon')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    """Admin for about section content (singleton)"""

    def has_add_permission(self, request):
        # Only allow one instance
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of about section
        return False

    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'description', 'image')
        }),
        ('Location Section', {
            'fields': ('location_title', 'location_content')
        }),
        ('Communities Section', {
            'fields': ('communities_title', 'communities_content')
        }),
        ('Structure Section', {
            'fields': ('structure_title', 'structure_content')
        }),
    )

    def changelist_view(self, request, extra_context=None):
        # Redirect to the single instance edit page
        obj = AboutSection.load()
        return self.changeform_view(request, str(obj.pk), extra_context=extra_context)
