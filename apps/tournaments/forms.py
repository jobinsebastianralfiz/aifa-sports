"""
Tournaments app forms.
"""

from django import forms
from .models import Tournament, Team, Match


class TournamentForm(forms.ModelForm):
    """Tournament form for admin."""

    class Meta:
        model = Tournament
        fields = [
            'name', 'slug', 'short_description', 'description',
            'logo', 'banner', 'tournament_type',
            'start_date', 'end_date', 'venue', 'organizer',
            'status', 'is_major', 'is_featured', 'show_on_homepage', 'display_order',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'short_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-textarea rich-editor', 'rows': 6}),
            'tournament_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'venue': forms.TextInput(attrs={'class': 'form-input'}),
            'organizer': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_major': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class TeamForm(forms.ModelForm):
    """Team form for admin."""

    class Meta:
        model = Team
        fields = [
            'name', 'slug', 'short_name', 'logo',
            'home_ground', 'city', 'founded_year', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'short_name': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '10'}),
            'home_ground': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class MatchForm(forms.ModelForm):
    """Match form for admin."""

    class Meta:
        model = Match
        fields = [
            'tournament', 'home_team', 'away_team',
            'match_type', 'match_number', 'group_name',
            'match_date', 'match_time', 'venue',
            'home_score', 'away_score',
            'home_score_extra', 'away_score_extra',
            'home_score_penalties', 'away_score_penalties',
            'status', 'current_minute', 'highlights_url',
            'is_featured', 'show_on_homepage'
        ]
        widgets = {
            'tournament': forms.Select(attrs={'class': 'form-select'}),
            'home_team': forms.Select(attrs={'class': 'form-select'}),
            'away_team': forms.Select(attrs={'class': 'form-select'}),
            'match_type': forms.Select(attrs={'class': 'form-select'}),
            'match_number': forms.NumberInput(attrs={'class': 'form-input'}),
            'group_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Group A'}),
            'match_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'match_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-input'}),
            'home_score': forms.NumberInput(attrs={'class': 'form-input score-input'}),
            'away_score': forms.NumberInput(attrs={'class': 'form-input score-input'}),
            'home_score_extra': forms.NumberInput(attrs={'class': 'form-input score-input'}),
            'away_score_extra': forms.NumberInput(attrs={'class': 'form-input score-input'}),
            'home_score_penalties': forms.NumberInput(attrs={'class': 'form-input score-input'}),
            'away_score_penalties': forms.NumberInput(attrs={'class': 'form-input score-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'current_minute': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 45'}),
            'highlights_url': forms.URLInput(attrs={'class': 'form-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
