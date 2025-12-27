"""
Events app forms.
"""

from django import forms
from .models import Event, EventFormField


class EventForm(forms.ModelForm):
    """Event form for admin."""

    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'event_type', 'short_description', 'description',
            'featured_image', 'venue', 'venue_address', 'google_maps_link',
            'start_date', 'end_date', 'start_time', 'end_time',
            'registration_required', 'registration_deadline',
            'max_participants', 'registration_fee', 'is_free',
            'program', 'status', 'is_featured', 'show_on_homepage',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'short_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-textarea rich-editor', 'rows': 8}),
            'venue': forms.TextInput(attrs={'class': 'form-input'}),
            'venue_address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'google_maps_link': forms.URLInput(attrs={'class': 'form-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'registration_required': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-input'}),
            'registration_fee': forms.NumberInput(attrs={'class': 'form-input'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class EventFormFieldForm(forms.ModelForm):
    """Form for adding/editing event form fields."""

    class Meta:
        model = EventFormField
        fields = [
            'field_type', 'label', 'placeholder',
            'is_required', 'help_text', 'options'
        ]
        widgets = {
            'field_type': forms.Select(attrs={'class': 'form-select'}),
            'label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Student Name'}),
            'placeholder': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Enter student name'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'help_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional help text'}),
            'options': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'For select/radio: ["Option 1", "Option 2", "Option 3"]'
            }),
        }
