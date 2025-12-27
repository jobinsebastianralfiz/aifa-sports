from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Accreditation(TimeStampedModel):
    """Certifications, affiliations, and accreditations of the academy."""

    class AccreditationType(models.TextChoices):
        CERTIFICATION = 'certification', 'Certification'
        AFFILIATION = 'affiliation', 'Affiliation'
        PARTNERSHIP = 'partnership', 'Partnership'
        MEMBERSHIP = 'membership', 'Membership'

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    issuing_body = models.CharField(
        max_length=200,
        help_text="Organization that issued the accreditation (e.g., FIFA, UEFA, AIFF)"
    )
    accreditation_type = models.CharField(
        max_length=20,
        choices=AccreditationType.choices,
        default=AccreditationType.CERTIFICATION
    )
    logo = models.ImageField(
        upload_to='accreditations/',
        help_text="Logo of the accrediting body (recommended: 200x200)"
    )
    website_url = models.URLField(blank=True, help_text="Link to accrediting organization")
    issued_date = models.DateField(null=True, blank=True)
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Star rating (1-5)"
    )
    rating_label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Rating label (e.g., '4 Star Rating', 'Elite Academy')"
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Accreditation"
        verbose_name_plural = "Accreditations"

    def __str__(self):
        return f"{self.name} - {self.issuing_body}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Accreditation.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
