from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import NewsCategory, NewsArticle


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    """Admin for news categories"""

    list_display = ('name', 'color_badge', 'slug', 'article_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'color')
        }),
    )

    def color_badge(self, obj):
        """Display color badge"""
        return format_html(
            '<span style="display: inline-block; width: 30px; height: 30px; background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></span>',
            obj.color
        )
    color_badge.short_description = 'Color'

    def article_count(self, obj):
        """Count of articles in this category"""
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    """Admin for news articles"""

    list_display = (
        'title',
        'article_image',
        'category',
        'status_badge',
        'is_featured',
        'views',
        'published_date',
        'author'
    )
    list_filter = ('status', 'category', 'is_featured', 'published_date', 'created_at')
    list_editable = ('is_featured',)
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date', '-created_at')
    readonly_fields = ('views', 'reading_time', 'created_at', 'updated_at')

    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'image_caption')
        }),
        ('Classification', {
            'fields': ('category', 'author')
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'published_date')
        }),
        ('Metrics', {
            'fields': ('views', 'reading_time'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['publish_articles', 'unpublish_articles', 'feature_articles', 'unfeature_articles', 'archive_articles']

    def article_image(self, obj):
        """Display article thumbnail in list view"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return '-'
    article_image.short_description = 'Image'

    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def reading_time(self, obj):
        """Display estimated reading time"""
        return f"{obj.reading_time} min"
    reading_time.short_description = 'Reading Time'

    # Custom Actions
    @admin.action(description='Publish selected articles')
    def publish_articles(self, request, queryset):
        updated = queryset.update(status='published', published_date=timezone.now())
        self.message_user(request, f'{updated} article(s) published successfully.')

    @admin.action(description='Unpublish selected articles')
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} article(s) unpublished.')

    @admin.action(description='Mark as featured')
    def feature_articles(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} article(s) marked as featured.')

    @admin.action(description='Unmark as featured')
    def unfeature_articles(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} article(s) unmarked as featured.')

    @admin.action(description='Archive selected articles')
    def archive_articles(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} article(s) archived.')
