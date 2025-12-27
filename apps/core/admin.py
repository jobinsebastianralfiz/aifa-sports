from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import SiteSettings, PageSettings, AboutPageContent, HomepageContent, BoardMember


class JSONEditorWidget(forms.Textarea):
    """Custom widget for better JSON editing experience."""
    def __init__(self, attrs=None):
        default_attrs = {
            'rows': 8,
            'style': 'font-family: monospace; width: 100%;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for site-wide settings."""

    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline', 'logo', 'logo_white', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'address', 'google_maps_embed')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('SEO Defaults', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Analytics & Footer', {
            'fields': ('google_analytics_id', 'footer_about', 'copyright_text'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageSettings)
class PageSettingsAdmin(admin.ModelAdmin):
    """Admin for page-specific settings."""

    list_display = ('page_type', 'hero_title_preview', 'has_hero_image', 'updated_at')
    list_filter = ('page_type',)
    search_fields = ('hero_title', 'meta_title')

    fieldsets = (
        ('Page Selection', {
            'fields': ('page_type',)
        }),
        ('Hero Section', {
            'fields': ('hero_image', 'hero_title', 'hero_subtitle')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    def hero_title_preview(self, obj):
        if obj.hero_title:
            # Strip HTML tags for preview
            import re
            clean = re.sub('<[^<]+?>', '', obj.hero_title)
            return clean[:50] + '...' if len(clean) > 50 else clean
        return '-'
    hero_title_preview.short_description = 'Hero Title'

    def has_hero_image(self, obj):
        if obj.hero_image:
            return format_html('<span style="color: green;">Yes</span>')
        return format_html('<span style="color: #999;">No</span>')
    has_hero_image.short_description = 'Hero Image'


class AboutPageContentForm(forms.ModelForm):
    """Custom form for AboutPageContent with better JSON editing."""

    class Meta:
        model = AboutPageContent
        fields = '__all__'
        widgets = {
            'core_values': JSONEditorWidget(),
            'statistics': JSONEditorWidget(),
            'story_content': forms.Textarea(attrs={'rows': 8}),
        }


@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
    """Admin for About page content."""
    form = AboutPageContentForm

    fieldsets = (
        ('Story Section', {
            'fields': ('story_title', 'story_content', 'story_image', 'founding_year')
        }),
        ('Mission & Vision', {
            'fields': ('mission_title', 'mission_content', 'vision_title', 'vision_content')
        }),
        ('Core Values', {
            'fields': ('core_values',),
            'description': '''Enter values as JSON array. Example:
[{"icon": "star", "title": "Excellence", "description": "We strive for excellence."}]
Available icons: star, users, heart, check-circle, trophy, award, zap, layout'''
        }),
        ('Statistics', {
            'fields': ('statistics',),
            'description': '''Enter statistics as JSON object. Example:
{"students_trained": 5000, "trophies_won": 50, "district_players": 100, "years_excellence": 10}'''
        }),
    )

    def has_add_permission(self, request):
        return not AboutPageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class HomepageContentForm(forms.ModelForm):
    """Custom form for HomepageContent with better JSON editing."""

    class Meta:
        model = HomepageContent
        fields = '__all__'
        widgets = {
            'marquee_items': JSONEditorWidget(),
            'about_section_features': JSONEditorWidget(),
        }


@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    """Admin for Homepage content."""
    form = HomepageContentForm

    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_badge_text',)
        }),
        ('Marquee (Scrolling Text)', {
            'fields': ('marquee_items',),
            'description': 'Enter as JSON array: ["Item 1", "Item 2", "Item 3"]'
        }),
        ('About Section Preview', {
            'fields': ('about_section_tag', 'about_section_title',
                      'about_section_text', 'about_section_features'),
        }),
        ('CTA Section', {
            'fields': ('cta_title', 'cta_text', 'cta_button_text', 'cta_button_link')
        }),
        ('Statistics Section', {
            'fields': ('show_statistics', 'statistics_background_text')
        }),
    )

    def has_add_permission(self, request):
        return not HomepageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    """Admin for Board of Directors."""

    list_display = ('full_name', 'designation', 'display_order', 'show_on_website')
    list_filter = ('show_on_website',)
    list_editable = ('display_order', 'show_on_website')
    search_fields = ('first_name', 'last_name', 'designation')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    ordering = ('display_order', 'first_name')

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'slug', 'photo', 'designation')
        }),
        ('Details', {
            'fields': ('bio', 'linkedin_url', 'email'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('show_on_website', 'display_order')
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
