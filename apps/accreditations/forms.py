from django import forms
from .models import Accreditation


class AccreditationForm(forms.ModelForm):
    class Meta:
        model = Accreditation
        fields = [
            'name', 'description', 'issuing_body', 'accreditation_type',
            'logo', 'website_url', 'issued_date', 'rating', 'rating_label',
            'is_active', 'is_featured', 'show_on_homepage', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Accreditation name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Description'}),
            'issuing_body': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., FIFA, UEFA, AIFF'}),
            'accreditation_type': forms.Select(attrs={'class': 'form-select'}),
            'logo': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'website_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'issued_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 5, 'placeholder': '1-5'}),
            'rating_label': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 4 Star Rating, Elite Academy'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0'}),
        }
