from django.db import models
from django.utils.text import slugify


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
        help_text="Internal path (e.g., /contact) or external URL"
    )
    link_text = models.CharField(
        max_length=50,
        default="Learn More"
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

    def __str__(self):
        return self.name
