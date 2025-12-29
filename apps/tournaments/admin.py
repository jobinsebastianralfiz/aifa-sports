from django.contrib import admin
from .models import Tournament, Team, Match


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'tournament_type', 'status', 'start_date', 'is_major', 'is_featured', 'show_on_homepage']
    list_filter = ['status', 'tournament_type', 'is_major', 'is_featured', 'show_on_homepage']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'start_date'
    ordering = ['-start_date']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'short_description', 'description', 'logo', 'banner')
        }),
        ('Tournament Details', {
            'fields': ('tournament_type', 'start_date', 'end_date', 'venue', 'organizer')
        }),
        ('Display Settings', {
            'fields': ('status', 'is_major', 'is_featured', 'show_on_homepage', 'display_order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'city', 'is_active']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'short_name', 'city']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'short_name', 'logo')
        }),
        ('Team Details', {
            'fields': ('home_ground', 'city', 'founded_year')
        }),
        ('Display', {
            'fields': ('is_active',)
        }),
    )


class MatchInline(admin.TabularInline):
    model = Match
    extra = 0
    fields = ['home_team', 'away_team', 'match_date', 'match_time', 'home_score', 'away_score', 'status']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'tournament', 'match_type', 'match_date', 'score_display', 'status', 'is_featured']
    list_filter = ['status', 'match_type', 'tournament', 'is_featured', 'show_on_homepage']
    search_fields = ['home_team__name', 'away_team__name', 'tournament__name']
    date_hierarchy = 'match_date'
    ordering = ['-match_date', '-match_time']
    autocomplete_fields = ['tournament', 'home_team', 'away_team']

    fieldsets = (
        ('Match Info', {
            'fields': ('tournament', 'home_team', 'away_team', 'match_type', 'group_name', 'match_number')
        }),
        ('Schedule', {
            'fields': ('match_date', 'match_time', 'venue')
        }),
        ('Score', {
            'fields': (
                ('home_score', 'away_score'),
                ('home_score_extra', 'away_score_extra'),
                ('home_score_penalties', 'away_score_penalties'),
            )
        }),
        ('Status & Info', {
            'fields': ('status', 'current_minute', 'highlights_url')
        }),
        ('Display', {
            'fields': ('is_featured', 'show_on_homepage')
        }),
    )
