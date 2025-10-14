from django.db import models
from django.utils.text import slugify


class GalleryCategory(models.Model):
    """Gallery categories (Projects, Meetings, Events, etc.)"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Gallery images"""

    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.PROTECT,
        related_name='images'
    )

    # Image
    image = models.ImageField(
        upload_to='gallery/%Y/%m/',
        help_text="Gallery image (recommended: 1200x800px)"
    )
    caption = models.TextField(blank=True)

    # Dates
    date_taken = models.DateField(
        blank=True,
        null=True,
        help_text="Date when photo was taken"
    )
    uploaded_date = models.DateTimeField(auto_now_add=True)

    # Display Settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured gallery section"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_taken', '-uploaded_date']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['-date_taken']),
        ]

    def __str__(self):
        return self.title
