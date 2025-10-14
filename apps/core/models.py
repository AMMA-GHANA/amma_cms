from django.db import models
from django.core.validators import FileExtensionValidator


class SingletonModel(models.Model):
    """Abstract base class for singleton models (only one instance allowed)"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """Site-wide configuration and settings"""

    # Basic Information
    site_name = models.CharField(
        max_length=200,
        default="Asokore Mampong Municipal Assembly"
    )
    tagline = models.CharField(
        max_length=300,
        default="Serving Our Community with Excellence"
    )

    # Logos and Images
    logo = models.ImageField(
        upload_to='site/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        help_text="Main site logo (recommended: 200x200px)"
    )
    favicon = models.ImageField(
        upload_to='site/',
        validators=[FileExtensionValidator(['ico', 'png'])],
        blank=True,
        help_text="Browser favicon (recommended: 32x32px)"
    )

    # Contact Information
    phone = models.CharField(max_length=20, default="+233 024 636 1845")
    email = models.EmailField(default="info@amma.gov.gh")
    address = models.TextField(
        default="Asokore Mampong, Ashanti Region, Ghana"
    )
    office_hours = models.CharField(
        max_length=200,
        default="Mon - Fri: 8:00 AM - 5:00 PM"
    )

    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # SEO
    meta_description = models.TextField(
        max_length=160,
        default="Official website of Asokore Mampong Municipal Assembly"
    )
    meta_keywords = models.TextField(
        default="AMMA, Asokore Mampong, Municipal Assembly, Ghana"
    )

    # Google Analytics
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Google Analytics tracking ID (e.g., G-XXXXXXXXXX)"
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class HeroSlide(models.Model):
    """Homepage hero carousel slides"""

    title = models.CharField(max_length=200)
    subtitle = models.TextField(max_length=500)
    image = models.ImageField(
        upload_to='hero/',
        help_text="Hero image (recommended: 1920x1080px)"
    )

    # Call to Action
    button_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Leave blank to hide button"
    )
    button_link = models.CharField(
        max_length=200,
        blank=True,
        help_text="Can be internal (/about) or external (https://...)"
    )

    # Display Settings
    order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to temporarily hide this slide"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return self.title


class Statistic(models.Model):
    """Homepage statistics/facts cards"""

    label = models.CharField(
        max_length=100,
        help_text="E.g., 'Total Population'"
    )
    value = models.CharField(
        max_length=50,
        help_text="E.g., '191,402' or '15+'"
    )
    icon = models.CharField(
        max_length=50,
        default="users",
        help_text="Lucide icon name (without 'lucide-' prefix)"
    )

    # Display Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"

    def __str__(self):
        return f"{self.label}: {self.value}"


class AboutSection(SingletonModel):
    """About section content for homepage"""

    title = models.CharField(
        max_length=200,
        default="About Asokore Mampong Municipal Assembly"
    )
    description = models.TextField(
        default="One of 261 Metropolitan, Municipal and District Assemblies in Ghana"
    )

    # Content Sections
    location_title = models.CharField(
        max_length=100,
        default="Our Location"
    )
    location_content = models.TextField(
        default="The Municipality forms boundaries with Kumasi Metropolitan Assembly..."
    )

    communities_title = models.CharField(
        max_length=100,
        default="Communities We Serve"
    )
    communities_content = models.TextField(
        default="Our area covers Aboabo No.1, Aboabo No.2..."
    )

    structure_title = models.CharField(
        max_length=100,
        default="Our Structure"
    )
    structure_content = models.TextField(
        default="The Assembly comprises 15 Assembly Members..."
    )

    # Optional Image
    image = models.ImageField(
        upload_to='about/',
        blank=True,
        help_text="Optional image for about section"
    )

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section Content"
