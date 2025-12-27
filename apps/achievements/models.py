from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Achievement(TimeStampedModel):
    """Trophies, awards, and achievements of the academy."""

    class Category(models.TextChoices):
        TROPHY = 'trophy', 'Trophy'
        CHAMPIONSHIP = 'championship', 'Championship'
        AWARD = 'award', 'Award'
        RECOGNITION = 'recognition', 'Recognition'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(help_text="Year the achievement was earned")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.TROPHY
    )
    image = models.ImageField(
        upload_to='achievements/',
        blank=True,
        help_text="Image of trophy/award (recommended: 400x400)"
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-year', '-created_at']
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self):
        return f"{self.title} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.year}")
            self.slug = base_slug
            counter = 1
            while Achievement.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
