"""
Contact app forms.
"""

import base64
from django import forms
from django.core.exceptions import ValidationError
from .models import ContactMessage, Inquiry


class ContactForm(forms.ModelForm):
    """Public contact form."""

    # Hidden field for human verification (football CAPTCHA)
    human_verified = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),
        error_messages={
            'required': 'Please complete the verification by dragging the football to the goal.'
        }
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Phone (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Your Message',
                'rows': 5
            }),
        }

    def clean_human_verified(self):
        """Validate the human verification token."""
        token = self.cleaned_data.get('human_verified', '')

        if not token:
            raise ValidationError(
                'Please complete the verification by dragging the football to the goal.'
            )

        try:
            # Decode and validate the token format
            decoded = base64.b64decode(token).decode('utf-8')
            if not decoded.startswith('goal_'):
                raise ValidationError('Invalid verification. Please try again.')

            # Check token timestamp (must be within last 10 minutes)
            parts = decoded.split('_')
            if len(parts) >= 2:
                timestamp = int(parts[1])
                import time
                current_time = int(time.time() * 1000)
                # Token should be less than 10 minutes old
                if current_time - timestamp > 600000:
                    raise ValidationError('Verification expired. Please try again.')

        except (ValueError, base64.binascii.Error):
            raise ValidationError('Invalid verification. Please try again.')

        return token


class InquiryForm(forms.ModelForm):
    """Program inquiry form."""

    class Meta:
        model = Inquiry
        fields = [
            'student_name', 'student_age',
            'guardian_name', 'guardian_email', 'guardian_phone',
            'program', 'message'
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-input'}),
            'student_age': forms.NumberInput(attrs={'class': 'form-input'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-input'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }
