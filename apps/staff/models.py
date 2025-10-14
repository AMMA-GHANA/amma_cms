from django.db import models
from django.core.validators import FileExtensionValidator


class Department(models.Model):
    """Organizational departments"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    """Staff members and leadership"""

    POSITION_TYPE_CHOICES = [
        ('leadership', 'Leadership'),
        ('management', 'Management'),
        ('staff', 'Staff'),
    ]

    # Basic Information
    full_name = models.CharField(max_length=200)
    position = models.CharField(
        max_length=200,
        help_text="Job title/position"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members'
    )

    # Position Classification
    position_type = models.CharField(
        max_length=20,
        choices=POSITION_TYPE_CHOICES,
        default='staff',
        help_text="Category for display organization"
    )

    # Bio and Photo
    bio = models.TextField(
        blank=True,
        help_text="Professional biography"
    )
    photo = models.ImageField(
        upload_to='staff/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Professional photo (recommended: 400x400px, square)"
    )

    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Display Settings
    display_order = models.IntegerField(
        default=0,
        help_text="Display order within position type"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from public display"
    )

    # Employment Details
    joined_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date joined the assembly"
    )

    # Social Media (Optional)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position_type', 'display_order', 'full_name']
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"
        indexes = [
            models.Index(fields=['position_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    @property
    def is_leadership(self):
        """Check if member is in leadership"""
        return self.position_type == 'leadership'
