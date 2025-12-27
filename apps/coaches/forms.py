"""
Coaches app forms.
"""

from django import forms
from .models import Coach


class CoachForm(forms.ModelForm):
    """Coach form for admin."""

    class Meta:
        model = Coach
        fields = [
            'first_name', 'last_name', 'slug', 'designation', 'photo',
            'specialization', 'bio', 'qualifications', 'experience_years',
            'achievements', 'email', 'phone',
            'linkedin_url', 'instagram_url',
            'status', 'show_on_website', 'display_order',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'designation': forms.TextInput(attrs={'class': 'form-input'}),
            'specialization': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea rich-editor', 'rows': 6}),
            'qualifications': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input'}),
            'achievements': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'show_on_website': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '70'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'maxlength': '160'}),
        }
