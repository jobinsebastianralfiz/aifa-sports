"""
Core app forms.
"""

import json
from django import forms
from .models import SiteSettings, PageSettings, AboutPageContent, HomepageContent, BoardMember, CommunityActivity, CommunityPageContent


class SiteSettingsForm(forms.ModelForm):
    """Form for site settings."""

    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'tagline', 'logo', 'logo_white', 'favicon',
            'email', 'phone', 'whatsapp', 'address', 'google_maps_embed',
            'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url',
            'meta_title', 'meta_description', 'meta_keywords', 'og_image',
            'google_analytics_id',
            'footer_about', 'copyright_text',
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-input'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'google_maps_embed': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-input'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-input'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-input'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '70'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'maxlength': '160'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-input'}),
            'google_analytics_id': forms.TextInput(attrs={'class': 'form-input'}),
            'footer_about': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'copyright_text': forms.TextInput(attrs={'class': 'form-input'}),
        }


class PageSettingsForm(forms.ModelForm):
    """Form for page-specific settings."""

    class Meta:
        model = PageSettings
        fields = [
            'page_type', 'hero_image', 'hero_title', 'hero_subtitle',
            'meta_title', 'meta_description',
        ]
        widgets = {
            'page_type': forms.Select(attrs={'class': 'form-select'}),
            'hero_title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., ABOUT <span class="text-gradient">US</span>'}),
            'hero_subtitle': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '70'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'maxlength': '160'}),
        }


class AboutPageContentForm(forms.ModelForm):
    """Form for About page content."""

    # JSON fields as text areas
    core_values_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 8,
            'style': 'font-family: monospace;',
            'placeholder': '[{"icon": "star", "title": "Excellence", "description": "..."}]'
        }),
        help_text='Enter as JSON array. Icons: star, users, heart, check-circle, trophy, award, zap'
    )

    statistics_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 6,
            'style': 'font-family: monospace;',
            'placeholder': '{"students_trained": 5000, "trophies_won": 50, "district_players": 100, "years_excellence": 10}'
        }),
        help_text='Enter as JSON object'
    )

    class Meta:
        model = AboutPageContent
        fields = [
            'story_title', 'story_content', 'story_image', 'founding_year',
        ]
        widgets = {
            'story_title': forms.TextInput(attrs={'class': 'form-input'}),
            'story_content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
            'founding_year': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['core_values_text'].initial = json.dumps(self.instance.core_values, indent=2) if self.instance.core_values else ''
            self.fields['statistics_text'].initial = json.dumps(self.instance.statistics, indent=2) if self.instance.statistics else ''

    def clean_core_values_text(self):
        data = self.cleaned_data.get('core_values_text', '')
        if not data:
            return []
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON format for core values')

    def clean_statistics_text(self):
        data = self.cleaned_data.get('statistics_text', '')
        if not data:
            return {}
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON format for statistics')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.core_values = self.cleaned_data.get('core_values_text', [])
        instance.statistics = self.cleaned_data.get('statistics_text', {})
        if commit:
            instance.save()
        return instance


class HomepageContentForm(forms.ModelForm):
    """Form for Homepage content."""

    # JSON fields as text areas
    marquee_items_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 4,
            'style': 'font-family: monospace;',
            'placeholder': '["Elite Training", "Professional Coaches", "Modern Facilities"]'
        }),
        help_text='Enter as JSON array'
    )

    about_features_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 6,
            'style': 'font-family: monospace;',
            'placeholder': '[{"icon": "award", "text": "UEFA Licensed Coaches"}]'
        }),
        help_text='Enter as JSON array. Icons: award, zap, layout, trophy, clock, star'
    )

    class Meta:
        model = HomepageContent
        fields = [
            'hero_badge_text',
            'about_section_tag', 'about_section_title', 'about_section_text',
            'cta_title', 'cta_text', 'cta_button_text', 'cta_button_link',
            'show_statistics', 'statistics_background_text',
        ]
        widgets = {
            'hero_badge_text': forms.TextInput(attrs={'class': 'form-input'}),
            'about_section_tag': forms.TextInput(attrs={'class': 'form-input'}),
            'about_section_title': forms.TextInput(attrs={'class': 'form-input'}),
            'about_section_text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'cta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'cta_text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'cta_button_text': forms.TextInput(attrs={'class': 'form-input'}),
            'cta_button_link': forms.TextInput(attrs={'class': 'form-input'}),
            'show_statistics': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'statistics_background_text': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['marquee_items_text'].initial = json.dumps(self.instance.marquee_items, indent=2) if self.instance.marquee_items else ''
            self.fields['about_features_text'].initial = json.dumps(self.instance.about_section_features, indent=2) if self.instance.about_section_features else ''

    def clean_marquee_items_text(self):
        data = self.cleaned_data.get('marquee_items_text', '')
        if not data:
            return []
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON format for marquee items')

    def clean_about_features_text(self):
        data = self.cleaned_data.get('about_features_text', '')
        if not data:
            return []
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON format for about features')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.marquee_items = self.cleaned_data.get('marquee_items_text', [])
        instance.about_section_features = self.cleaned_data.get('about_features_text', [])
        if commit:
            instance.save()
        return instance


class BoardMemberForm(forms.ModelForm):
    """Form for Board Member."""

    class Meta:
        model = BoardMember
        fields = [
            'first_name', 'last_name', 'slug', 'photo', 'designation',
            'bio', 'linkedin_url', 'email', 'show_on_website', 'display_order'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'designation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Chairman, Director'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'show_on_website': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }


class CommunityActivityForm(forms.ModelForm):
    """Form for Community Activity."""

    class Meta:
        model = CommunityActivity
        fields = [
            'title', 'slug', 'category', 'description', 'short_description',
            'image', 'date', 'location', 'beneficiaries',
            'is_featured', 'show_on_website', 'display_order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Leave blank to auto-generate'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6}),
            'short_description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief summary for cards'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'beneficiaries': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 500 underprivileged children'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_website': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }


class CommunityPageContentForm(forms.ModelForm):
    """Form for Community Page Content."""

    class Meta:
        model = CommunityPageContent
        fields = [
            'hero_title', 'hero_subtitle', 'hero_image',
            'intro_title', 'intro_content',
            'stats_volunteers', 'stats_events', 'stats_beneficiaries', 'stats_hours',
        ]
        widgets = {
            'hero_title': forms.TextInput(attrs={'class': 'form-input'}),
            'hero_subtitle': forms.TextInput(attrs={'class': 'form-input'}),
            'intro_title': forms.TextInput(attrs={'class': 'form-input'}),
            'intro_content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6}),
            'stats_volunteers': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'stats_events': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'stats_beneficiaries': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'stats_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }
