"""
Hero app forms.
"""

from django import forms
from .models import HeroSlide


class HeroSlideForm(forms.ModelForm):
    """Hero slide form for admin with video/image and SEO support."""

    class Meta:
        model = HeroSlide
        fields = [
            # Basic
            'title', 'subtitle', 'description',
            # Media
            'media_type', 'image', 'image_alt',
            'video', 'video_url', 'video_poster',
            # CTA
            'cta_text', 'cta_link',
            # Status
            'is_active', 'display_order',
            # SEO
            'meta_title', 'meta_description',
        ]
        widgets = {
            # Basic fields
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter slide title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter subtitle (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'rows': 3,
                'placeholder': 'Additional description (optional)'
            }),
            # Media fields
            'media_type': forms.RadioSelect(attrs={
                'class': 'media-type-radio'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
            'image_alt': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Describe the image for accessibility'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'video/mp4,video/webm,video/ogg'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://www.youtube.com/embed/...'
            }),
            'video_poster': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
            # CTA fields
            'cta_text': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Start Your Journey'
            }),
            'cta_link': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., /programs/'
            }),
            # Status fields
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 0
            }),
            # SEO fields
            'meta_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'SEO title (max 70 characters)',
                'maxlength': 70
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'rows': 2,
                'placeholder': 'SEO description (max 160 characters)',
                'maxlength': 160
            }),
        }

    def clean(self):
        """Validate that appropriate media is provided based on media_type."""
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        video_url = cleaned_data.get('video_url')

        if media_type == 'image' and not image and not self.instance.image:
            self.add_error('image', 'Please upload an image for image type slides.')

        if media_type == 'video':
            if not video and not video_url and not self.instance.video:
                self.add_error('video', 'Please upload a video or provide a video URL.')

        return cleaned_data
