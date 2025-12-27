"""
Testimonials app forms.
"""

from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    """Testimonial form for admin."""

    class Meta:
        model = Testimonial
        fields = [
            'name', 'role', 'photo', 'content',
            'rating', 'is_active', 'is_featured', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Parent, Student, U-14 Player'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 5}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }
