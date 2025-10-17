from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Service(models.Model):
    """Municipal services offered to citizens"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    # Icon
    icon = models.CharField(
        max_length=50,
        default="file-text",
        help_text="Lucide icon name"
    )

    # Link
    link_url = models.CharField(
        max_length=200,
        blank=True,
        help_text="Leave blank to use detail page, or provide external URL"
    )
    link_text = models.CharField(
        max_length=50,
        default="Learn More"
    )

    has_detail_page = models.BooleanField(
        default=True,
        help_text="If True, service will have a detail page with content blocks"
    )

    # Display Settings
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL for this service"""
        if self.link_url:
            return self.link_url
        return reverse('services:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class ServiceContentBlock(models.Model):
    """Flexible content blocks for service detail pages"""

    BLOCK_TYPES = [
        ('text', 'Text Block'),
        ('service_grid', 'Service Box Grid'),
        ('list', 'List Block'),
        ('steps', 'Process Steps'),
        ('notice', 'Notice/Alert Block'),
        ('table', 'Table Block'),
        ('document', 'Document/Download Block'),
        ('image', 'Image Block'),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='content_blocks'
    )
    block_type = models.CharField(
        max_length=20,
        choices=BLOCK_TYPES,
        default='text'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional title for this block"
    )
    content = models.TextField(
        blank=True,
        help_text="Main content - supports markdown"
    )
    data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional structured data for complex blocks"
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Content Block"
        verbose_name_plural = "Content Blocks"

    def __str__(self):
        return f"{self.service.name} - {self.get_block_type_display()} #{self.order}"
