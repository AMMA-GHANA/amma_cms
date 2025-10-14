from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class NewsCategory(models.Model):
    """News article categories"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7,
        default="#d4af37",
        help_text="Hex color code (e.g., #d4af37)"
    )

    class Meta:
        verbose_name_plural = "News Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """News articles and updates"""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    excerpt = models.TextField(
        max_length=300,
        help_text="Brief summary (max 300 characters)"
    )
    content = CKEditor5Field('Content', config_name='default')

    # Images
    featured_image = models.ImageField(
        upload_to='news/%Y/%m/',
        help_text="Main article image (recommended: 800x600px)"
    )
    image_caption = models.CharField(max_length=200, blank=True)

    # Classification
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.PROTECT,
        related_name='articles'
    )
    author = models.ForeignKey(
        'staff.StaffMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_articles'
    )

    # Status
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage and featured sections"
    )

    # Dates
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metrics
    views = models.IntegerField(default=0, editable=False)

    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (max 160 characters)"
    )

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        # Auto-generate slug from title
        if not self.slug:
            self.slug = slugify(self.title)

        # Set published date when status changes to published
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()

        # Auto-generate meta description from excerpt if not provided
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def increment_views(self):
        """Increment the view count"""
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def is_published(self):
        """Check if article is published"""
        return self.status == 'published' and self.published_date is not None

    @property
    def reading_time(self):
        """Estimate reading time in minutes"""
        words = len(self.content.split())
        minutes = words // 200  # Average reading speed
        return max(1, minutes)

    def get_absolute_url(self):
        """Return the URL for this article"""
        from django.urls import reverse
        return reverse('news:detail', kwargs={'slug': self.slug})
