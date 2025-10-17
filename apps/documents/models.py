from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
import os


class DocumentCategory(models.Model):
    """Document categories for organization"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        default="folder",
        help_text="Lucide icon name"
    )
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Document Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Document(models.Model):
    """Downloadable documents and files"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    description = models.TextField()

    # Category
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.PROTECT,
        related_name='documents'
    )

    # File
    file = models.FileField(
        upload_to='documents/%Y/%m/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'xls', 'xlsx'])],
        help_text="Allowed: PDF, DOC, DOCX, XLS, XLSX"
    )

    # Optional Thumbnail
    thumbnail = models.ImageField(
        upload_to='documents/thumbs/',
        blank=True,
        help_text="Optional preview image"
    )

    # Auto-calculated File Info
    file_size = models.CharField(max_length=20, blank=True, editable=False)
    file_type = models.CharField(max_length=10, blank=True, editable=False)

    # Document Period (for time-based organization)
    document_year = models.IntegerField(
        null=True,
        blank=True,
        help_text="Year this document pertains to (e.g., 2024)"
    )
    document_quarter = models.CharField(
        max_length=2,
        choices=[
            ('Q1', 'Quarter 1'),
            ('Q2', 'Quarter 2'),
            ('Q3', 'Quarter 3'),
            ('Q4', 'Quarter 4'),
        ],
        null=True,
        blank=True,
        help_text="Quarter this document pertains to"
    )

    # Dates
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # Metrics
    download_count = models.IntegerField(default=0, editable=False)

    # Display Settings
    is_public = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from public"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured documents section"
    )

    class Meta:
        ordering = ['-uploaded_date']
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_public']),
            models.Index(fields=['document_year']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Calculate file size and type
        if self.file:
            self.file_size = self.format_file_size(self.file.size)
            self.file_type = os.path.splitext(self.file.name)[1][1:].upper()

        super().save(*args, **kwargs)

    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def increment_downloads(self):
        """Increment download counter"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

    def __str__(self):
        if self.document_year:
            period = f"{self.document_year}"
            if self.document_quarter:
                period += f" {self.document_quarter}"
            return f"{self.title} ({period})"
        return self.title
