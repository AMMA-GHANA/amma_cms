from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class ProjectCategory(models.Model):
    """Project categories"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        default="building",
        help_text="Lucide icon name"
    )
    color = models.CharField(
        max_length=7,
        default="#d4af37",
        help_text="Hex color code for category badge"
    )
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    """Municipal development projects"""

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    description = models.TextField(
        help_text="Short description (used in cards and listings)"
    )
    detailed_description = CKEditor5Field(
        'Detailed Description',
        config_name='default',
        blank=True
    )

    # Classification
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        related_name='projects'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='planned'
    )

    # Location and Timeline
    location = models.CharField(
        max_length=200,
        help_text="Project location/community"
    )
    start_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)

    # Financial Information
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Project budget in GHS"
    )

    # Impact Metrics
    beneficiaries = models.CharField(
        max_length=100,
        blank=True,
        help_text="E.g., '5,000+ citizens served daily'"
    )
    impact_icon = models.CharField(
        max_length=50,
        blank=True,
        default="users",
        help_text="Lucide icon for impact metric"
    )
    impact_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Impact description for card display"
    )

    # Display Settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage featured projects section"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers first)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-start_date']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def primary_image(self):
        """Get the primary project image"""
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def status_badge_color(self):
        """Return appropriate color class for status badge"""
        colors = {
            'planned': 'blue',
            'ongoing': 'orange',
            'completed': 'green',
            'suspended': 'red',
        }
        return colors.get(self.status, 'gray')


class ProjectImage(models.Model):
    """Images for projects (allows multiple images per project)"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='projects/%Y/%m/',
        help_text="Project image (recommended: 1200x800px)"
    )
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary image shown in cards and listings"
    )
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'order', 'uploaded_at']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per project
        if self.is_primary:
            ProjectImage.objects.filter(
                project=self.project,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"
