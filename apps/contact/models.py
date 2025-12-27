"""
Contact app models.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """Contact form submissions."""

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
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.subject} - {self.name}"


class Inquiry(TimeStampedModel):
    """Program inquiry/admission interest."""

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
    program = models.ForeignKey(
        'programs.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='inquiries'
    )
    message = models.TextField(blank=True)

    # Processing
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.student_name} - {self.program}"
