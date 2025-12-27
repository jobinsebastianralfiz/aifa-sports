"""
Gallery app forms.
"""

from django import forms
from .models import GalleryCategory, GalleryImage, GalleryVideo


class GalleryCategoryForm(forms.ModelForm):
    """Gallery category form for admin."""

    class Meta:
        model = GalleryCategory
        fields = [
            'name', 'slug', 'description', 'cover_image', 'is_active', 'display_order',
            'meta_title', 'meta_description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '70'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'maxlength': '160'}),
        }


class GalleryImageForm(forms.ModelForm):
    """Gallery image form for admin."""

    class Meta:
        model = GalleryImage
        fields = ['category', 'title', 'image', 'alt_text', 'is_active', 'display_order']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Describe the image for accessibility'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class GalleryVideoForm(forms.ModelForm):
    """Gallery video form for admin."""

    class Meta:
        model = GalleryVideo
        fields = [
            'title', 'platform', 'video_url', 'thumbnail', 'description',
            'is_active', 'is_featured', 'display_order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter video title'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'video_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Paste the video URL'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }
        help_texts = {
            'video_url': 'Supports YouTube, YouTube Shorts, Instagram Reels, Facebook, and TikTok',
            'thumbnail': 'Optional custom thumbnail. YouTube videos will auto-fetch thumbnails.',
        }
