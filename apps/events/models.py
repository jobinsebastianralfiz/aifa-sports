"""
Events app models - Events, trials, and dynamic form builder.
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Event(TimeStampedModel):
    """Events and trials organized by AIFA."""

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
    program = models.ForeignKey(
        'programs.Program',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )

    # Display
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

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
    """Dynamic form fields for event registration."""

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
    options = models.JSONField(
        default=list,
        blank=True,
        help_text='Options for select/radio/checkbox fields'
    )

    # Validation
    min_length = models.PositiveIntegerField(null=True, blank=True)
    max_length = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Event Form Field"
        verbose_name_plural = "Event Form Fields"

    def __str__(self):
        return f"{self.event.title} - {self.label}"

    @property
    def field_name(self):
        """Generate a field name from label for form data storage."""
        return slugify(self.label).replace('-', '_')


class EventRegistration(TimeStampedModel):
    """Event registration submissions."""

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
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

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
