from django import forms
from .models import Facility, FacilityCategory


class FacilityCategoryForm(forms.ModelForm):
    class Meta:
        model = FacilityCategory
        fields = ['name', 'icon', 'display_order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category name'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., football, dumbbell'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            'name', 'short_description', 'description', 'category',
            'image', 'icon', 'area_size', 'features',
            'is_active', 'is_featured', 'show_on_homepage', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Facility name'}),
            'short_description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief description'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Detailed description'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., football, dumbbell'}),
            'area_size': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 80,000 Sqft'}),
            'features': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'One feature per line'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0'}),
        }
