"""
Hero app models.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class HeroSlide(TimeStampedModel):
    """Homepage hero slider with image/video support and SEO."""

    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    # Basic Fields
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True, help_text="Additional description text")

    # Media Fields
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image',
        help_text="Type of media for this slide"
    )
    image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        help_text="Image for the slide (recommended: 1920x1080)"
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for the image (for accessibility & SEO)"
    )
    video = models.FileField(
        upload_to='hero/videos/',
        blank=True,
        null=True,
        help_text="Upload video file (MP4 recommended)"
    )
    video_url = models.URLField(
        blank=True,
        help_text="External video URL (YouTube, Vimeo embed URL)"
    )
    video_poster = models.ImageField(
        upload_to='hero/posters/',
        blank=True,
        null=True,
        help_text="Poster/thumbnail image shown before video plays"
    )

    # CTA (Call to Action)
    cta_text = models.CharField(max_length=50, blank=True, help_text="Button text")
    cta_link = models.CharField(max_length=200, blank=True, help_text="Button link")

    # Status & Ordering
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    # SEO Fields
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="SEO title (max 70 characters)"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO description (max 160 characters)"
    )

    class Meta:
        ordering = ['display_order']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return self.title

    @property
    def has_video(self):
        """Check if this slide has a video."""
        return self.media_type == 'video' and (self.video or self.video_url)

    @property
    def media_url(self):
        """Get the appropriate media URL based on type."""
        if self.media_type == 'video':
            if self.video:
                return self.video.url
            return self.video_url
        if self.image:
            return self.image.url
        return None

    @property
    def poster_url(self):
        """Get poster image URL for video slides."""
        if self.video_poster:
            return self.video_poster.url
        if self.image:
            return self.image.url
        return None
