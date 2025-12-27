# AIFA Sports Academy - Django Implementation Plan
## Phase 1: Dynamic Website with Admin CMS

### Scope

This phase focuses on:
- **Dynamic Public Website** - All content managed from backend
- **Custom Admin Dashboard** - Using our designed templates
- **Two User Roles** - Super Admin & Staff only

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [User Roles](#2-user-roles)
3. [Django Apps & Models](#3-django-apps--models)
4. [Template Integration](#4-template-integration)
5. [URL Structure](#5-url-structure)
6. [SEO Implementation](#6-seo-implementation)
7. [Implementation Steps](#7-implementation-steps)

---

## 1. Project Structure

```
aifa_sports/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
│
├── config/                          # Project configuration
│   ├── __init__.py
│   ├── settings.py                  # Settings (or settings/ folder for dev/prod)
│   ├── urls.py                      # Root URL configuration
│   └── wsgi.py
│
├── apps/                            # Django applications
│   ├── __init__.py
│   ├── core/                        # Site settings, common utilities
│   ├── accounts/                    # User authentication & roles
│   ├── programs/                    # Programs & batches
│   ├── coaches/                     # Coach profiles
│   ├── events/                      # Events, trials & dynamic forms
│   ├── news/                        # News & announcements
│   ├── gallery/                     # Photo/video gallery
│   ├── blog/                        # Blog articles
│   ├── testimonials/                # Testimonials
│   ├── hero/                        # Hero slider
│   └── contact/                     # Contact messages & inquiries
│
├── templates/                       # Django templates
│   ├── base.html                    # Base template
│   │
│   ├── frontend/                    # Public website
│   │   ├── base_frontend.html       # Frontend base (header, footer)
│   │   ├── index.html               # Homepage
│   │   ├── about.html               # About page
│   │   ├── programs/
│   │   │   ├── list.html            # Programs listing
│   │   │   └── detail.html          # Program detail
│   │   ├── coaches.html             # Coaches page
│   │   ├── gallery.html             # Gallery page
│   │   ├── events/
│   │   │   ├── list.html            # Events listing
│   │   │   ├── detail.html          # Event detail
│   │   │   └── register.html        # Event registration form
│   │   ├── news/
│   │   │   ├── list.html            # News listing
│   │   │   └── detail.html          # News detail
│   │   ├── blog/
│   │   │   ├── list.html            # Blog listing
│   │   │   └── detail.html          # Blog post detail
│   │   ├── contact.html             # Contact page
│   │   └── includes/                # Reusable components
│   │       ├── header.html
│   │       ├── footer.html
│   │       ├── hero_slider.html
│   │       └── testimonials.html
│   │
│   ├── admin_dashboard/             # Custom admin (from /admin/ folder)
│   │   ├── base_admin.html          # Admin base layout
│   │   ├── index.html               # Dashboard
│   │   ├── programs/
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── coaches/
│   │   ├── events/                  # Events management
│   │   │   ├── list.html
│   │   │   ├── form.html
│   │   │   ├── detail.html
│   │   │   ├── form_builder.html    # Dynamic form builder
│   │   │   └── registrations.html   # View registrations
│   │   ├── news/                    # News management
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── gallery/
│   │   ├── blog/
│   │   ├── testimonials/
│   │   ├── hero_slides/
│   │   ├── messages/
│   │   ├── settings/
│   │   └── includes/
│   │       ├── sidebar.html
│   │       └── topbar.html
│   │
│   ├── accounts/                    # Auth templates
│   │   ├── login.html
│   │   └── profile.html
│   │
│   └── includes/                    # Global includes
│       ├── messages.html            # Flash messages
│       ├── pagination.html
│       └── seo_meta.html
│
├── static/                          # Static files
│   ├── css/
│   │   ├── design-system.css        # From frontend/css/
│   │   ├── components.css
│   │   ├── utilities.css
│   │   ├── responsive.css
│   │   └── admin/
│   │       └── admin.css            # From admin/css/
│   ├── js/
│   │   ├── main.js
│   │   └── admin/
│   │       └── admin.js
│   └── images/
│       ├── logo.svg
│       └── logo-white.svg
│
└── media/                           # User uploads
    ├── coaches/
    ├── gallery/
    ├── blog/
    └── programs/
```

---

## 2. User Roles

### Simple Role-Based Access

```python
# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile with role"""

    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        STAFF = 'staff', 'Staff'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    def is_staff_member(self):
        return self.role in [self.Role.SUPER_ADMIN, self.Role.STAFF]
```

### Permissions

| Feature | Super Admin | Staff |
|---------|-------------|-------|
| View Dashboard | ✓ | ✓ |
| Manage Programs | ✓ | ✓ |
| Manage Coaches | ✓ | ✓ |
| Manage Events | ✓ | ✓ |
| Create Event Forms | ✓ | ✓ |
| View Registrations | ✓ | ✓ |
| Manage News | ✓ | ✓ |
| Manage Gallery | ✓ | ✓ |
| Manage Blog | ✓ | ✓ |
| Manage Testimonials | ✓ | ✓ |
| Manage Hero Slides | ✓ | ✓ |
| View Messages | ✓ | ✓ |
| Reply to Messages | ✓ | ✓ |
| Site Settings | ✓ | ✗ |
| Manage Users | ✓ | ✗ |

### Permission Decorator

```python
# apps/accounts/decorators.py

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """Require Super Admin or Staff login"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile'):
            messages.error(request, "Access denied.")
            return redirect('frontend:home')
        return view_func(request, *args, **kwargs)
    return wrapper

def super_admin_required(view_func):
    """Require Super Admin login"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile') or not request.user.profile.is_super_admin():
            messages.error(request, "Super Admin access required.")
            return redirect('admin_dashboard:index')
        return view_func(request, *args, **kwargs)
    return wrapper
```

---

## 3. Django Apps & Models

### 3.1 Core App - Site Settings

```python
# apps/core/models.py

from django.db import models

class SiteSettings(models.Model):
    """Singleton model for site-wide settings"""

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
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to='site/', blank=True)

    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)

    # Footer
    footer_about = models.TextField(blank=True, help_text="Short about text for footer")
    copyright_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # Ensure singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class TimeStampedModel(models.Model):
    """Abstract base model with timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### 3.2 Programs App

```python
# apps/programs/models.py

from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel

class Program(TimeStampedModel):
    """Sports program/course"""

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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Batch(TimeStampedModel):
    """Training batch for a program"""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FULL = 'full', 'Full'
        UPCOMING = 'upcoming', 'Upcoming'
        COMPLETED = 'completed', 'Completed'

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='batches')
    name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200, help_text="e.g., 'Mon, Wed, Fri - 4:00 PM'")
    coach = models.ForeignKey('coaches.Coach', on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.CharField(max_length=200)
    max_capacity = models.PositiveIntegerField(default=20)
    current_strength = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"{self.name} - {self.program.name}"

    @property
    def available_slots(self):
        return max(0, self.max_capacity - self.current_strength)
```

### 3.3 Coaches App

```python
# apps/coaches/models.py

from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel

class Coach(TimeStampedModel):
    """Coach profile for website display"""

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

    class Meta:
        ordering = ['display_order', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)
```

### 3.4 Hero Slides App

```python
# apps/hero/models.py

from django.db import models
from apps.core.models import TimeStampedModel

class HeroSlide(TimeStampedModel):
    """Homepage hero slider"""

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='hero/')
    cta_text = models.CharField(max_length=50, blank=True, help_text="Button text")
    cta_link = models.CharField(max_length=200, blank=True, help_text="Button link")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title
```

### 3.5 Testimonials App

```python
# apps/testimonials/models.py

from django.db import models
from apps.core.models import TimeStampedModel

class Testimonial(TimeStampedModel):
    """Customer testimonials"""

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

    def __str__(self):
        return f"{self.name} - {self.role}"
```

### 3.6 Gallery App

```python
# apps/gallery/models.py

from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel

class GalleryCategory(TimeStampedModel):
    """Gallery album/category"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
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
    """Gallery image"""

    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/images/')
    alt_text = models.CharField(max_length=200, blank=True, help_text="For accessibility")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title
```

### 3.7 Events App (with Dynamic Form Builder)

```python
# apps/events/models.py

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import TimeStampedModel

class Event(TimeStampedModel):
    """Events and trials organized by AIFA"""

    class EventType(models.TextChoices):
        TRIAL = 'trial', 'Trial/Selection'
        TOURNAMENT = 'tournament', 'Tournament'
        WORKSHOP = 'workshop', 'Workshop'
        CAMP = 'camp', 'Training Camp'
        COMPETITION = 'competition', 'Competition'
        OPEN_DAY = 'open_day', 'Open Day'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        UPCOMING = 'upcoming', 'Upcoming'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    featured_image = models.ImageField(upload_to='events/')

    # Date & Time
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    # Location
    venue = models.CharField(max_length=200)
    venue_address = models.TextField(blank=True)
    google_maps_link = models.URLField(blank=True)

    # Capacity & Registration
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_required = models.BooleanField(default=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=True)

    # Related
    program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='events')

    # Display
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_registration_open(self):
        if not self.registration_required:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        if self.status not in ['upcoming', 'ongoing']:
            return False
        if self.max_participants:
            return self.registrations.count() < self.max_participants
        return True

    @property
    def registration_count(self):
        return self.registrations.count()

    @property
    def available_slots(self):
        if not self.max_participants:
            return None
        return max(0, self.max_participants - self.registrations.count())


class EventFormField(TimeStampedModel):
    """Dynamic form fields for event registration"""

    class FieldType(models.TextChoices):
        TEXT = 'text', 'Text Input'
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone Number'
        NUMBER = 'number', 'Number'
        DATE = 'date', 'Date'
        TEXTAREA = 'textarea', 'Text Area'
        SELECT = 'select', 'Dropdown Select'
        RADIO = 'radio', 'Radio Buttons'
        CHECKBOX = 'checkbox', 'Checkboxes'
        FILE = 'file', 'File Upload'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='form_fields')
    field_type = models.CharField(max_length=20, choices=FieldType.choices)
    label = models.CharField(max_length=200)
    placeholder = models.CharField(max_length=200, blank=True)
    help_text = models.CharField(max_length=300, blank=True)
    is_required = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    # For select, radio, checkbox - store options as JSON
    options = models.JSONField(default=list, blank=True,
        help_text='Options for select/radio/checkbox fields')

    # Validation
    min_length = models.PositiveIntegerField(null=True, blank=True)
    max_length = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.event.title} - {self.label}"


class EventRegistration(TimeStampedModel):
    """Event registration submissions"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        ATTENDED = 'attended', 'Attended'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_number = models.CharField(max_length=20, unique=True, editable=False)

    # Basic participant info (always required)
    participant_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Dynamic form data stored as JSON
    form_data = models.JSONField(default=dict)

    # File uploads stored separately
    uploaded_files = models.JSONField(default=dict, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    admin_notes = models.TextField(blank=True)

    # Payment (if applicable)
    payment_status = models.CharField(max_length=20, default='not_required')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.registration_number} - {self.participant_name}"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = self.generate_registration_number()
        super().save(*args, **kwargs)

    def generate_registration_number(self):
        """Generate: EVT-YYYYMMDD-XXXX"""
        from datetime import date
        today = date.today()
        prefix = f'EVT-{today.strftime("%Y%m%d")}'

        last_reg = EventRegistration.objects.filter(
            registration_number__startswith=prefix
        ).order_by('-registration_number').first()

        if last_reg:
            last_num = int(last_reg.registration_number.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1

        return f'{prefix}-{new_num:04d}'
```

### 3.8 News App

```python
# apps/news/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import TimeStampedModel

class News(TimeStampedModel):
    """News and announcements"""

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
    category = models.CharField(max_length=20, choices=Category.choices,
        default=Category.GENERAL)
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
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
```

### 3.9 Blog App

```python
# apps/blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import TimeStampedModel

class BlogCategory(TimeStampedModel):
    """Blog category"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    """Blog post/article"""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Short summary")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/')
    featured_image_alt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))
```

### 3.8 Contact App

```python
# apps/contact/models.py

from django.db import models
from apps.core.models import TimeStampedModel

class ContactMessage(TimeStampedModel):
    """Contact form submissions"""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        READ = 'read', 'Read'
        REPLIED = 'replied', 'Replied'

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    replied_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"


class Inquiry(TimeStampedModel):
    """Program inquiry/admission interest"""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        ENROLLED = 'enrolled', 'Enrolled'
        CLOSED = 'closed', 'Closed'

    # Student Info
    student_name = models.CharField(max_length=100)
    student_age = models.PositiveIntegerField()

    # Guardian Info
    guardian_name = models.CharField(max_length=100)
    guardian_email = models.EmailField()
    guardian_phone = models.CharField(max_length=20)

    # Interest
    program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL, null=True)
    message = models.TextField(blank=True)

    # Processing
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.student_name} - {self.program}"
```

---

## 4. Template Integration

### Mapping Existing Templates

| Current HTML File | Django Template | Purpose |
|-------------------|-----------------|---------|
| **Admin Templates** |||
| `admin/index.html` | `admin_dashboard/index.html` | Dashboard |
| `admin/programs.html` | `admin_dashboard/programs/list.html` | Programs list |
| `admin/program-detail.html` | `admin_dashboard/programs/detail.html` | Program view |
| `admin/coaches.html` | `admin_dashboard/coaches/list.html` | Coaches list |
| `admin/coach-detail.html` | `admin_dashboard/coaches/detail.html` | Coach view |
| `admin/gallery.html` | `admin_dashboard/gallery/list.html` | Gallery management |
| `admin/blog.html` | `admin_dashboard/blog/list.html` | Blog posts |
| (create) | `admin_dashboard/events/list.html` | Events list |
| (create) | `admin_dashboard/events/form.html` | Event add/edit |
| (create) | `admin_dashboard/events/form_builder.html` | Dynamic form builder |
| (create) | `admin_dashboard/events/registrations.html` | View registrations |
| (create) | `admin_dashboard/news/list.html` | News list |
| (create) | `admin_dashboard/news/form.html` | News add/edit |
| `admin/testimonials.html` | `admin_dashboard/testimonials/list.html` | Testimonials |
| `admin/hero-slides.html` | `admin_dashboard/hero_slides/list.html` | Hero slider |
| `admin/messages.html` | `admin_dashboard/messages/list.html` | Contact messages |
| `admin/settings.html` | `admin_dashboard/settings/index.html` | Site settings |
| `admin/batches.html` | `admin_dashboard/batches/list.html` | Batches |
| `admin/batch-detail.html` | `admin_dashboard/batches/detail.html` | Batch view |
| **Frontend Templates** |||
| `frontend/index.html` | `frontend/index.html` | Homepage |
| (create) | `frontend/about.html` | About page |
| (create) | `frontend/programs/list.html` | Programs listing |
| (create) | `frontend/programs/detail.html` | Program detail |
| (create) | `frontend/coaches.html` | Coaches page |
| (create) | `frontend/events/list.html` | Events listing |
| (create) | `frontend/events/detail.html` | Event detail |
| (create) | `frontend/events/register.html` | Event registration form |
| (create) | `frontend/news/list.html` | News listing |
| (create) | `frontend/news/detail.html` | News detail |
| (create) | `frontend/gallery.html` | Gallery page |
| (create) | `frontend/blog/list.html` | Blog listing |
| (create) | `frontend/blog/detail.html` | Blog post |
| (create) | `frontend/contact.html` | Contact page |

### Static Files Mapping

| Current Location | Django Static Location |
|------------------|------------------------|
| `admin/css/admin.css` | `static/css/admin/admin.css` |
| `admin/js/admin.js` | `static/js/admin/admin.js` |
| `frontend/css/*.css` | `static/css/*.css` |
| `frontend/js/*.js` | `static/js/*.js` |
| `frontend/assets/images/` | `static/images/` |

---

## 5. URL Structure

### Frontend URLs (Public)

```python
# apps/core/urls_frontend.py

from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]

# apps/programs/urls.py
urlpatterns = [
    path('programs/', views.ProgramListView.as_view(), name='list'),
    path('programs/<slug:slug>/', views.ProgramDetailView.as_view(), name='detail'),
]

# apps/coaches/urls.py
urlpatterns = [
    path('coaches/', views.CoachListView.as_view(), name='list'),
]

# apps/events/urls.py
urlpatterns = [
    path('events/', views.EventListView.as_view(), name='list'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='detail'),
    path('events/<slug:slug>/register/', views.EventRegisterView.as_view(), name='register'),
]

# apps/news/urls.py
urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
]

# apps/gallery/urls.py
urlpatterns = [
    path('gallery/', views.GalleryView.as_view(), name='list'),
]

# apps/blog/urls.py
urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name='list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
]
```

### Admin Dashboard URLs

```python
# apps/core/urls_admin.py

from django.urls import path, include

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('programs/', include('apps.programs.urls_admin')),
    path('coaches/', include('apps.coaches.urls_admin')),
    path('batches/', include('apps.programs.urls_admin_batches')),
    path('events/', include('apps.events.urls_admin')),
    path('news/', include('apps.news.urls_admin')),
    path('gallery/', include('apps.gallery.urls_admin')),
    path('blog/', include('apps.blog.urls_admin')),
    path('testimonials/', include('apps.testimonials.urls_admin')),
    path('hero-slides/', include('apps.hero.urls_admin')),
    path('messages/', include('apps.contact.urls_admin')),
    path('inquiries/', include('apps.contact.urls_admin_inquiries')),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
```

### Complete URL Map

| URL | View | Template |
|-----|------|----------|
| **Public Website** |||
| `/` | HomeView | `frontend/index.html` |
| `/about/` | AboutView | `frontend/about.html` |
| `/programs/` | ProgramListView | `frontend/programs/list.html` |
| `/programs/<slug>/` | ProgramDetailView | `frontend/programs/detail.html` |
| `/coaches/` | CoachListView | `frontend/coaches.html` |
| `/events/` | EventListView | `frontend/events/list.html` |
| `/events/<slug>/` | EventDetailView | `frontend/events/detail.html` |
| `/events/<slug>/register/` | EventRegisterView | `frontend/events/register.html` |
| `/news/` | NewsListView | `frontend/news/list.html` |
| `/news/<slug>/` | NewsDetailView | `frontend/news/detail.html` |
| `/gallery/` | GalleryView | `frontend/gallery.html` |
| `/blog/` | BlogListView | `frontend/blog/list.html` |
| `/blog/<slug>/` | BlogDetailView | `frontend/blog/detail.html` |
| `/contact/` | ContactView | `frontend/contact.html` |
| **Admin Dashboard** |||
| `/dashboard/` | DashboardView | `admin_dashboard/index.html` |
| `/dashboard/programs/` | ProgramListView | `admin_dashboard/programs/list.html` |
| `/dashboard/programs/add/` | ProgramCreateView | `admin_dashboard/programs/form.html` |
| `/dashboard/programs/<id>/edit/` | ProgramUpdateView | `admin_dashboard/programs/form.html` |
| `/dashboard/events/` | EventListView | `admin_dashboard/events/list.html` |
| `/dashboard/events/add/` | EventCreateView | `admin_dashboard/events/form.html` |
| `/dashboard/events/<id>/edit/` | EventUpdateView | `admin_dashboard/events/form.html` |
| `/dashboard/events/<id>/form-builder/` | FormBuilderView | `admin_dashboard/events/form_builder.html` |
| `/dashboard/events/<id>/registrations/` | RegistrationsView | `admin_dashboard/events/registrations.html` |
| `/dashboard/news/` | NewsListView | `admin_dashboard/news/list.html` |
| `/dashboard/news/add/` | NewsCreateView | `admin_dashboard/news/form.html` |
| `/dashboard/news/<id>/edit/` | NewsUpdateView | `admin_dashboard/news/form.html` |
| `/dashboard/settings/` | SettingsView | `admin_dashboard/settings/index.html` |
| **Authentication** |||
| `/login/` | LoginView | `accounts/login.html` |
| `/logout/` | LogoutView | - |

---

## 6. SEO Implementation

### 6.1 SEO Meta Template

```html
<!-- templates/includes/seo_meta.html -->
{% load static %}

<title>{% block title %}{{ page_title|default:site_settings.site_name }}{% endblock %}</title>
<meta name="description" content="{{ meta_description|default:site_settings.meta_description }}">
<meta name="keywords" content="{{ meta_keywords|default:site_settings.meta_keywords }}">
<meta name="robots" content="index, follow">

<link rel="canonical" href="{{ request.build_absolute_uri }}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="{{ request.build_absolute_uri }}">
<meta property="og:title" content="{{ page_title|default:site_settings.site_name }}">
<meta property="og:description" content="{{ meta_description|default:site_settings.meta_description }}">
<meta property="og:image" content="{% if og_image %}{{ og_image.url }}{% endif %}">
<meta property="og:site_name" content="{{ site_settings.site_name }}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">

<!-- Favicon -->
<link rel="icon" href="{% static 'images/favicon.ico' %}">
```

### 6.2 Sitemap

```python
# apps/core/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.programs.models import Program
from apps.blog.models import BlogPost

class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['frontend:home', 'frontend:about', 'frontend:contact',
                'programs:list', 'coaches:list', 'gallery:list', 'blog:list']

    def location(self, item):
        return reverse(item)


class ProgramSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Program.objects.filter(status='active')

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at
```

### 6.3 Schema.org Structured Data

```html
<!-- In frontend/index.html -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "SportsActivityLocation",
    "name": "{{ site_settings.site_name }}",
    "description": "{{ site_settings.meta_description }}",
    "url": "{{ request.scheme }}://{{ request.get_host }}",
    "telephone": "{{ site_settings.phone }}",
    "email": "{{ site_settings.email }}",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "{{ site_settings.address }}"
    }
}
</script>
```

---

## 7. Implementation Steps

### Step 1: Project Setup
- [ ] Create Django project with `django-admin startproject config .`
- [ ] Create apps folder and all required apps
- [ ] Configure settings.py (database, static, media, templates)
- [ ] Set up .env for environment variables
- [ ] Install requirements (Django, Pillow, python-slugify)

### Step 2: Models & Database
- [ ] Create all models as defined above
- [ ] Run `makemigrations` and `migrate`
- [ ] Create superuser account

### Step 3: Static Files Setup
- [ ] Copy CSS files from `admin/css/` to `static/css/admin/`
- [ ] Copy CSS files from `frontend/css/` to `static/css/`
- [ ] Copy JS files
- [ ] Copy images and logos
- [ ] Configure STATIC_URL and STATICFILES_DIRS

### Step 4: Convert Admin Templates
- [ ] Create base_admin.html with Django template tags
- [ ] Convert sidebar.html with dynamic links
- [ ] Convert each admin page (programs, coaches, etc.)
- [ ] Add CSRF tokens to forms
- [ ] Replace static paths with `{% static %}` tags

### Step 5: Admin Views & Forms
- [ ] Create views for CRUD operations
- [ ] Create Django forms for each model
- [ ] Implement file upload handling
- [ ] Add flash messages for actions

### Step 6: Convert Frontend Templates
- [ ] Create base_frontend.html
- [ ] Convert homepage with dynamic content
- [ ] Create remaining public pages
- [ ] Add contact form with validation

### Step 7: Frontend Views
- [ ] Create views for public pages
- [ ] Query database for content
- [ ] Handle contact form submission
- [ ] Implement program inquiry form

### Step 8: SEO & Final
- [ ] Add sitemap.xml
- [ ] Add robots.txt
- [ ] Test all pages
- [ ] Optimize images

---

## Requirements

```txt
# requirements.txt

Django==5.0
Pillow==10.1.0
python-slugify==8.0.1
python-dotenv==1.0.0
django-widget-tweaks==1.5.0

# For production
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
```

---

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3" > .env

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic

# 7. Run server
python manage.py runserver
```

---

*Phase 1 Focus: Dynamic Website + Super Admin & Staff Roles*
*Version: 1.0*
*Last Updated: December 2024*
