from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class FacilityCategory(TimeStampedModel):
    """Categories for organizing facilities."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name (e.g., 'football', 'dumbbell', 'home')"
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Facility Category"
        verbose_name_plural = "Facility Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while FacilityCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Facility(TimeStampedModel):
    """Infrastructure and facilities of the academy."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Brief description for cards"
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        FacilityCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='facilities'
    )
    image = models.ImageField(
        upload_to='facilities/',
        help_text="Main image of the facility"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name for display"
    )
    area_size = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., '80,000 Sqft', '600 sq ft'"
    )
    features = models.TextField(
        blank=True,
        help_text="Key features, one per line"
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Facility.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_features_list(self):
        """Return features as a list."""
        if not self.features:
            return []
        return [f.strip() for f in self.features.split('\n') if f.strip()]
