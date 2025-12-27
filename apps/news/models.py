"""
News app models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import TimeStampedModel


class News(TimeStampedModel):
    """News and announcements."""

    class Category(models.TextChoices):
        ANNOUNCEMENT = 'announcement', 'Announcement'
        ACHIEVEMENT = 'achievement', 'Achievement'
        UPDATE = 'update', 'Update'
        SCHEDULE = 'schedule', 'Schedule Change'
        RESULT = 'result', 'Results'
        GENERAL = 'general', 'General'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL
    )
    excerpt = models.TextField(max_length=300, help_text="Short summary")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='news/', blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)

    # Priority/Display
    is_featured = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of news list")
    show_on_homepage = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        ordering = ['-is_pinned', '-published_at']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
