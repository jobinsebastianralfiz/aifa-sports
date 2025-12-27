"""
Programs app forms.
"""

from django import forms
from .models import Program, Batch


class ProgramForm(forms.ModelForm):
    """Program form for admin."""

    class Meta:
        model = Program
        fields = [
            'name', 'slug', 'short_description', 'description',
            'image', 'age_group', 'duration', 'sessions_per_week',
            'session_duration', 'fee_amount', 'fee_period',
            'status', 'is_featured', 'display_order',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'short_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-textarea rich-editor', 'rows': 10}),
            'age_group': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 8-12 years'}),
            'duration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 3 months'}),
            'sessions_per_week': forms.NumberInput(attrs={'class': 'form-input'}),
            'session_duration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 90 minutes'}),
            'fee_amount': forms.NumberInput(attrs={'class': 'form-input'}),
            'fee_period': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., monthly'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class BatchForm(forms.ModelForm):
    """Batch form for admin."""

    class Meta:
        model = Batch
        fields = [
            'program', 'name', 'schedule', 'venue',
            'coach', 'max_capacity', 'current_strength',
            'start_date', 'status'
        ]
        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'schedule': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Mon, Wed, Fri 4-6 PM'}),
            'venue': forms.TextInput(attrs={'class': 'form-input'}),
            'coach': forms.Select(attrs={'class': 'form-select'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-input'}),
            'current_strength': forms.NumberInput(attrs={'class': 'form-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
