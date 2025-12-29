"""
Core app models - Site settings and base models.
"""

from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base model with timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Singleton model for site-wide settings."""

    # Basic Info
    site_name = models.CharField(max_length=100, default="AIFA Sports Academy")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    logo_white = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)

    # Contact Info
    email = models.EmailField(default="info@aifasports.com")
    phone = models.CharField(max_length=20, default="+91 98765 43210")
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    google_maps_embed = models.TextField(blank=True, help_text="Google Maps iframe embed code")

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # SEO Defaults
    meta_title = models.CharField(max_length=70, blank=True, help_text="Default meta title for pages")
    meta_description = models.TextField(max_length=160, blank=True, help_text="Default meta description for pages")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    og_image = models.ImageField(upload_to='site/', blank=True, help_text="Default Open Graph image for social sharing")

    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)

    # Federation Logos
    aifl_logo = models.ImageField(upload_to='site/', blank=True, help_text="All India Football League logo for navbar")
    aifl_logo_alt = models.CharField(max_length=200, blank=True, default="AIFL", help_text="Alt text for AIFL logo")
    kfa_logo = models.ImageField(upload_to='site/', blank=True, help_text="Kerala Football Association logo for navbar")
    kfa_logo_alt = models.CharField(max_length=200, blank=True, default="KFA", help_text="Alt text for KFA logo")

    # Footer
    footer_about = models.TextField(blank=True, help_text="Short about text for footer")
    copyright_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1  # Ensure singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class PageSettings(TimeStampedModel):
    """Page-specific settings including hero and SEO."""

    class PageType(models.TextChoices):
        HOME = 'home', 'Home'
        ABOUT = 'about', 'About'
        CONTACT = 'contact', 'Contact'
        PROGRAMS = 'programs', 'Programs'
        COACHES = 'coaches', 'Coaches'
        EVENTS = 'events', 'Events'
        NEWS = 'news', 'News'
        GALLERY = 'gallery', 'Gallery'

    page_type = models.CharField(
        max_length=20,
        choices=PageType.choices,
        unique=True,
        help_text="Select the page this setting applies to"
    )

    # Hero Section
    hero_image = models.ImageField(
        upload_to='pages/hero/',
        blank=True,
        help_text="Hero background image (recommended: 1920x1080)"
    )
    hero_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Main hero title (supports HTML tags for styling)"
    )
    hero_subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="Subtitle text below the main title"
    )

    # SEO Meta
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="SEO title (max 70 characters)"
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="SEO description (max 160 characters)"
    )

    class Meta:
        verbose_name = "Page Setting"
        verbose_name_plural = "Page Settings"
        ordering = ['page_type']

    def __str__(self):
        return f"{self.get_page_type_display()} Page Settings"

    @classmethod
    def get_for_page(cls, page_type):
        """Get or create settings for a specific page."""
        obj, _ = cls.objects.get_or_create(page_type=page_type)
        return obj


class AboutPageContent(models.Model):
    """Singleton model for About page specific content."""

    # Story/Mission Section
    story_title = models.CharField(
        max_length=200,
        default="WHERE PASSION MEETS EXCELLENCE",
        help_text="Main story section title"
    )
    story_content = models.TextField(
        blank=True,
        help_text="Rich text content for the story/mission section (HTML supported)"
    )
    story_image = models.ImageField(
        upload_to='pages/about/',
        blank=True,
        help_text="Image for the story section"
    )
    founding_year = models.PositiveIntegerField(
        default=2014,
        help_text="Year the academy was founded"
    )

    # Mission & Vision
    mission_title = models.CharField(
        max_length=200,
        default="Our Mission",
        help_text="Mission section title"
    )
    mission_content = models.TextField(
        blank=True,
        help_text="Mission statement content (HTML supported)"
    )
    vision_title = models.CharField(
        max_length=200,
        default="Our Vision",
        help_text="Vision section title"
    )
    vision_content = models.TextField(
        blank=True,
        help_text="Vision statement content (HTML supported)"
    )

    # Core Values (JSON field for flexibility)
    core_values = models.JSONField(
        default=list,
        blank=True,
        help_text='List of core values. Format: [{"icon": "star", "title": "Excellence", "description": "..."}]'
    )

    # Statistics (JSON field)
    statistics = models.JSONField(
        default=dict,
        blank=True,
        help_text='Statistics. Format: {"students_trained": 5000, "trophies_won": 50, "district_players": 100, "years_excellence": 10}'
    )

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"

    def save(self, *args, **kwargs):
        self.pk = 1  # Ensure singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_content(cls):
        """Get or create the about page content."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def get_values_list(self):
        """Return core values as a list, with defaults if empty."""
        if not self.core_values:
            return [
                {"icon": "star", "title": "Excellence", "description": "We strive for excellence in everything we do."},
                {"icon": "users", "title": "Teamwork", "description": "We believe in the power of teamwork."},
                {"icon": "heart", "title": "Passion", "description": "Our passion drives us to inspire athletes."},
                {"icon": "check-circle", "title": "Integrity", "description": "We uphold the highest standards."},
            ]
        return self.core_values

    def get_statistics(self):
        """Return statistics with defaults if empty."""
        defaults = {
            "students_trained": 5000,
            "trophies_won": 50,
            "district_players": 100,
            "years_excellence": 10
        }
        if not self.statistics:
            return defaults
        return {**defaults, **self.statistics}


class BoardMember(TimeStampedModel):
    """Board of Directors member for About page."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    photo = models.ImageField(upload_to='board/', blank=True)
    designation = models.CharField(max_length=100, help_text="e.g., 'Chairman', 'Director'")
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    show_on_website = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'first_name']
        verbose_name = "Board Member"
        verbose_name_plural = "Board Members"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)


class CommunityActivity(TimeStampedModel):
    """Community outreach and charity activities."""

    class Category(models.TextChoices):
        CHARITY = 'charity', 'Charity Event'
        OUTREACH = 'outreach', 'Community Outreach'
        COACHING = 'coaching', 'Free Coaching Camp'
        DONATION = 'donation', 'Donation Drive'
        AWARENESS = 'awareness', 'Awareness Program'
        OTHER = 'other', 'Other'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OUTREACH)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, help_text="Brief summary for cards")
    image = models.ImageField(upload_to='community/')
    date = models.DateField(help_text="Date of the activity")
    location = models.CharField(max_length=200, blank=True)
    beneficiaries = models.CharField(max_length=200, blank=True, help_text="e.g., '500 underprivileged children'")
    is_featured = models.BooleanField(default=False)
    show_on_website = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date', 'display_order']
        verbose_name = "Community Activity"
        verbose_name_plural = "Community Activities"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CommunityPageContent(models.Model):
    """Singleton model for Community page content."""

    hero_title = models.CharField(
        max_length=200,
        default="COMMUNITY OUTREACH",
        help_text="Hero section title"
    )
    hero_subtitle = models.CharField(
        max_length=300,
        default="Making a Difference Beyond the Field",
        help_text="Hero section subtitle"
    )
    hero_image = models.ImageField(
        upload_to='pages/community/',
        blank=True,
        help_text="Hero background image"
    )
    intro_title = models.CharField(
        max_length=200,
        default="Giving Back to Our Community",
        help_text="Introduction section title"
    )
    intro_content = models.TextField(
        blank=True,
        help_text="Introduction content (HTML supported)"
    )
    stats_volunteers = models.PositiveIntegerField(default=50, help_text="Number of volunteers")
    stats_events = models.PositiveIntegerField(default=25, help_text="Number of events conducted")
    stats_beneficiaries = models.PositiveIntegerField(default=2000, help_text="Number of beneficiaries")
    stats_hours = models.PositiveIntegerField(default=500, help_text="Volunteer hours")

    class Meta:
        verbose_name = "Community Page Content"
        verbose_name_plural = "Community Page Content"

    def __str__(self):
        return "Community Page Content"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_content(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HomepageContent(models.Model):
    """Singleton model for Homepage specific content."""

    # Hero Badge
    hero_badge_text = models.CharField(
        max_length=100,
        default="#1 Rated Football Academy",
        help_text="Text shown in the hero badge"
    )

    # Marquee Items (scrolling text)
    marquee_items = models.JSONField(
        default=list,
        blank=True,
        help_text='List of marquee text items. Format: ["Elite Training", "Professional Coaches"]'
    )

    # About Section Preview
    about_section_tag = models.CharField(
        max_length=50,
        default="About Our Academy",
        help_text="Tag text above the about section title"
    )
    about_section_title = models.CharField(
        max_length=200,
        default='WHERE <span class="text-accent">Passion</span><br>MEETS EXCELLENCE',
        help_text="About section title (HTML supported for styling)"
    )
    about_section_text = models.TextField(
        blank=True,
        help_text="Preview text for about section on homepage"
    )
    about_section_features = models.JSONField(
        default=list,
        blank=True,
        help_text='Features list. Format: [{"icon": "clock", "text": "UEFA Licensed Coaches"}]'
    )

    # CTA Section
    cta_title = models.CharField(
        max_length=100,
        default="READY TO BEGIN?",
        help_text="CTA section title"
    )
    cta_text = models.TextField(
        default="Book a free trial session today and experience world-class football training firsthand.",
        help_text="CTA section description"
    )
    cta_button_text = models.CharField(
        max_length=50,
        default="Book Free Trial",
        help_text="Primary CTA button text"
    )
    cta_button_link = models.CharField(
        max_length=200,
        default="/contact/",
        help_text="Primary CTA button link"
    )

    # Statistics Section
    show_statistics = models.BooleanField(
        default=True,
        help_text="Show the statistics section on homepage"
    )
    statistics_background_text = models.CharField(
        max_length=50,
        default="CHAMPIONS",
        help_text="Large background text in statistics section"
    )

    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"

    def __str__(self):
        return "Homepage Content"

    def save(self, *args, **kwargs):
        self.pk = 1  # Ensure singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_content(cls):
        """Get or create the homepage content."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def get_marquee_items(self):
        """Return marquee items with defaults if empty."""
        if not self.marquee_items:
            return [
                "Elite Training",
                "Professional Coaches",
                "Modern Facilities",
                "All Age Groups",
                "Championship Winners",
                "Join Today"
            ]
        return self.marquee_items

    def get_about_features(self):
        """Return about features with defaults if empty."""
        if not self.about_section_features:
            return [
                {"icon": "award", "text": "UEFA Licensed Coaches"},
                {"icon": "zap", "text": "Modern Training Methods"},
                {"icon": "layout", "text": "World-Class Facilities"},
                {"icon": "trophy", "text": "Proven Track Record"},
            ]
        return self.about_section_features
