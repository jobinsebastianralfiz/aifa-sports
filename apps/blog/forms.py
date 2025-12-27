"""
Blog app forms.
"""

from django import forms
from .models import BlogPost, BlogCategory


class BlogCategoryForm(forms.ModelForm):
    """Blog category form for admin."""

    class Meta:
        model = BlogCategory
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }


class BlogPostForm(forms.ModelForm):
    """Blog post form for admin."""

    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'category', 'excerpt', 'content',
            'featured_image', 'featured_image_alt', 'status', 'is_featured',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-textarea rich-editor', 'rows': 15}),
            'featured_image_alt': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Describe the image'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }
