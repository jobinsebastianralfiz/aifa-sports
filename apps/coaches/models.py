"""
Coaches app models.
"""

from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Coach(TimeStampedModel):
    """Coach profile for website display."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ON_LEAVE = 'on_leave', 'On Leave'
        INACTIVE = 'inactive', 'Inactive'

    # Personal Info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    photo = models.ImageField(upload_to='coaches/')
    designation = models.CharField(max_length=100, help_text="e.g., 'Head Coach'")
    specialization = models.CharField(max_length=200)

    # Bio
    bio = models.TextField()
    experience_years = models.PositiveIntegerField()
    qualifications = models.TextField(blank=True)
    achievements = models.TextField(blank=True)

    # Contact (internal use)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Social (for website)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    # Display
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    show_on_website = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    # SEO Meta
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (max 70 chars)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (max 160 chars)")

    class Meta:
        ordering = ['display_order', 'first_name']
        verbose_name = "Coach"
        verbose_name_plural = "Coaches"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)
