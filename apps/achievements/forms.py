from django import forms
from .models import Achievement


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            'title', 'description', 'year', 'category',
            'image', 'is_active', 'is_featured', 'show_on_homepage', 'display_order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Achievement title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Description of the achievement'}),
            'year': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '2024'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0'}),
        }
