"""
Tournaments app models - Tournament, Team, and Match with scorecards.
"""

from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Tournament(TimeStampedModel):
    """Tournament model for organizing football tournaments."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        UPCOMING = 'upcoming', 'Upcoming'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class TournamentType(models.TextChoices):
        LEAGUE = 'league', 'League'
        KNOCKOUT = 'knockout', 'Knockout'
        GROUP_KNOCKOUT = 'group_knockout', 'Group + Knockout'
        FRIENDLY = 'friendly', 'Friendly'

    # Basic Info
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='tournaments/logos/', blank=True)
    banner = models.ImageField(upload_to='tournaments/banners/', blank=True)

    # Tournament Details
    tournament_type = models.CharField(
        max_length=20,
        choices=TournamentType.choices,
        default=TournamentType.KNOCKOUT
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    organizer = models.CharField(max_length=200, blank=True)

    # Display Settings
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_major = models.BooleanField(default=False, help_text="Highlight as a major tournament")
    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        ordering = ['-is_major', '-start_date']
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def match_count(self):
        return self.matches.count()

    @property
    def completed_matches(self):
        return self.matches.filter(status='completed').count()


class Team(TimeStampedModel):
    """Team model for tournament participants."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_name = models.CharField(max_length=10, blank=True, help_text="3-4 letter abbreviation")
    logo = models.ImageField(upload_to='tournaments/teams/', blank=True)

    # Team Info
    home_ground = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    # Display
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.short_name:
            self.short_name = self.name[:3].upper()
        super().save(*args, **kwargs)


class Match(TimeStampedModel):
    """Match model for tournament matches with scores."""

    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        LIVE = 'live', 'Live'
        HALFTIME = 'halftime', 'Half Time'
        COMPLETED = 'completed', 'Full Time'
        POSTPONED = 'postponed', 'Postponed'
        CANCELLED = 'cancelled', 'Cancelled'

    class MatchType(models.TextChoices):
        GROUP = 'group', 'Group Stage'
        ROUND_16 = 'round_16', 'Round of 16'
        QUARTER = 'quarter', 'Quarter Final'
        SEMI = 'semi', 'Semi Final'
        THIRD_PLACE = 'third_place', 'Third Place'
        FINAL = 'final', 'Final'
        LEAGUE = 'league', 'League Match'
        FRIENDLY = 'friendly', 'Friendly'

    # Tournament & Teams
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_matches'
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_matches'
    )

    # Match Details
    match_type = models.CharField(
        max_length=20,
        choices=MatchType.choices,
        default=MatchType.GROUP
    )
    match_number = models.PositiveIntegerField(null=True, blank=True)
    group_name = models.CharField(max_length=50, blank=True, help_text="e.g., Group A, Group B")

    # Schedule
    match_date = models.DateField()
    match_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=200, blank=True)

    # Score
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)

    # Extra time / Penalties (for knockout matches)
    home_score_extra = models.PositiveIntegerField(null=True, blank=True)
    away_score_extra = models.PositiveIntegerField(null=True, blank=True)
    home_score_penalties = models.PositiveIntegerField(null=True, blank=True)
    away_score_penalties = models.PositiveIntegerField(null=True, blank=True)

    # Match Info
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    current_minute = models.PositiveIntegerField(null=True, blank=True, help_text="Current match minute for live games")
    highlights_url = models.URLField(blank=True)

    # Display
    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)

    class Meta:
        ordering = ['-match_date', '-match_time']
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.home_team.short_name} vs {self.away_team.short_name} - {self.tournament.name}"

    @property
    def score_display(self):
        """Returns the score display string."""
        if self.status in ['scheduled', 'postponed', 'cancelled']:
            return "vs"
        return f"{self.home_score} - {self.away_score}"

    @property
    def is_live(self):
        return self.status in ['live', 'halftime']

    @property
    def winner(self):
        """Returns the winning team or None for draw/unfinished."""
        if self.status != 'completed':
            return None

        home_total = self.home_score + (self.home_score_extra or 0)
        away_total = self.away_score + (self.away_score_extra or 0)

        if self.home_score_penalties is not None and self.away_score_penalties is not None:
            if self.home_score_penalties > self.away_score_penalties:
                return self.home_team
            elif self.away_score_penalties > self.home_score_penalties:
                return self.away_team

        if home_total > away_total:
            return self.home_team
        elif away_total > home_total:
            return self.away_team
        return None
