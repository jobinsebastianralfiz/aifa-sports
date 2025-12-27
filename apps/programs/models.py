"""
Programs app models.
"""

from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Program(TimeStampedModel):
    """Sports program/course."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        UPCOMING = 'upcoming', 'Upcoming'
        INACTIVE = 'inactive', 'Inactive'

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/')

    # Details
    age_group = models.CharField(max_length=50, help_text="e.g., '6-12 years'")
    duration = models.CharField(max_length=50, help_text="e.g., '3 months'")
    sessions_per_week = models.PositiveIntegerField(default=3)
    session_duration = models.CharField(max_length=50, default="90 minutes")
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_period = models.CharField(max_length=20, default="monthly")

    # Features (stored as JSON list)
    features = models.JSONField(default=list, blank=True, help_text="List of features")

    # Display
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Batch(TimeStampedModel):
    """Training batch for a program."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FULL = 'full', 'Full'
        UPCOMING = 'upcoming', 'Upcoming'
        COMPLETED = 'completed', 'Completed'

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='batches')
    name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200, help_text="e.g., 'Mon, Wed, Fri - 4:00 PM'")
    coach = models.ForeignKey(
        'coaches.Coach',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches'
    )
    venue = models.CharField(max_length=200)
    max_capacity = models.PositiveIntegerField(default=20)
    current_strength = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"{self.name} - {self.program.name}"

    @property
    def available_slots(self):
        return max(0, self.max_capacity - self.current_strength)

    @property
    def is_full(self):
        return self.current_strength >= self.max_capacity
