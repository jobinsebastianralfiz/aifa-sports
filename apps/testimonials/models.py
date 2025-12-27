"""
Testimonials app models.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class Testimonial(TimeStampedModel):
    """Customer testimonials."""

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g., 'Parent of Student'")
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="1-5 stars")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.role}"
