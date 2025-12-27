"""
News app forms.
"""

from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    """News form for admin."""

    class Meta:
        model = News
        fields = [
            'title', 'slug', 'category', 'excerpt', 'content',
            'featured_image', 'status', 'is_featured', 'is_pinned', 'show_on_homepage',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-textarea rich-editor', 'rows': 12}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }
