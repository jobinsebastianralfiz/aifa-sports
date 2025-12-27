"""
Gallery app models.
"""

import re
from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class GalleryCategory(TimeStampedModel):
    """Gallery album/category."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (max 70 chars)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (max 160 chars)")

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def image_count(self):
        return self.images.filter(is_active=True).count()


class GalleryImage(TimeStampedModel):
    """Gallery image."""

    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name='images'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/images/')
    alt_text = models.CharField(max_length=200, blank=True, help_text="For accessibility")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title


class GalleryVideo(TimeStampedModel):
    """Gallery video from various platforms."""

    class Platform(models.TextChoices):
        YOUTUBE = 'youtube', 'YouTube'
        YOUTUBE_SHORTS = 'youtube_shorts', 'YouTube Shorts'
        INSTAGRAM = 'instagram', 'Instagram Reels'
        FACEBOOK = 'facebook', 'Facebook'
        TIKTOK = 'tiktok', 'TikTok'

    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=Platform.choices, default=Platform.YOUTUBE)
    video_url = models.URLField(help_text="Paste the video URL (YouTube, Instagram, Facebook, or TikTok)")
    video_id = models.CharField(max_length=100, blank=True, help_text="Auto-extracted from URL")
    thumbnail = models.ImageField(upload_to='gallery/video_thumbnails/', blank=True, help_text="Custom thumbnail (optional)")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Gallery Video"
        verbose_name_plural = "Gallery Videos"

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"

    def save(self, *args, **kwargs):
        # Auto-extract video ID from URL
        if self.video_url and not self.video_id:
            self.video_id = self.extract_video_id()
        super().save(*args, **kwargs)

    def extract_video_id(self):
        """Extract video ID from various platform URLs."""
        url = self.video_url

        # YouTube regular videos
        youtube_patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
        ]
        for pattern in youtube_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # Instagram
        instagram_pattern = r'instagram\.com/(?:p|reel|reels)/([a-zA-Z0-9_-]+)'
        match = re.search(instagram_pattern, url)
        if match:
            return match.group(1)

        # Facebook
        facebook_patterns = [
            r'facebook\.com/.*?/videos/(\d+)',
            r'fb\.watch/([a-zA-Z0-9_-]+)',
        ]
        for pattern in facebook_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # TikTok
        tiktok_pattern = r'tiktok\.com/.*?/video/(\d+)'
        match = re.search(tiktok_pattern, url)
        if match:
            return match.group(1)

        return ''

    @property
    def embed_url(self):
        """Get the embed URL for the video."""
        if not self.video_id:
            return ''

        if self.platform in ['youtube', 'youtube_shorts']:
            return f'https://www.youtube.com/embed/{self.video_id}'
        elif self.platform == 'instagram':
            return f'https://www.instagram.com/p/{self.video_id}/embed'
        elif self.platform == 'facebook':
            return f'https://www.facebook.com/plugins/video.php?href={self.video_url}'
        elif self.platform == 'tiktok':
            return f'https://www.tiktok.com/embed/v2/{self.video_id}'
        return ''

    @property
    def thumbnail_url(self):
        """Get thumbnail URL - custom or auto-generated."""
        if self.thumbnail:
            return self.thumbnail.url
        # YouTube auto-thumbnail
        if self.platform in ['youtube', 'youtube_shorts'] and self.video_id:
            return f'https://img.youtube.com/vi/{self.video_id}/maxresdefault.jpg'
        return ''

    @property
    def is_vertical(self):
        """Check if video is vertical format (Shorts, Reels, TikTok)."""
        return self.platform in ['youtube_shorts', 'instagram', 'tiktok']
