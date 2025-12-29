"""
Tournaments app frontend views.
"""

from django.views.generic import ListView, DetailView
from .models import Tournament, Match, Team


class TournamentListView(ListView):
    """List all tournaments."""
    model = Tournament
    template_name = 'frontend/tournaments/list.html'
    context_object_name = 'tournaments'

    def get_queryset(self):
        return Tournament.objects.filter(
            status__in=['upcoming', 'ongoing', 'completed']
        ).order_by('-is_major', '-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get latest completed matches
        context['recent_matches'] = Match.objects.filter(
            status='completed'
        ).select_related('tournament', 'home_team', 'away_team').order_by('-match_date', '-match_time')[:10]
        # Get ongoing tournaments
        context['ongoing_tournaments'] = Tournament.objects.filter(status='ongoing')
        # Get upcoming tournaments
        context['upcoming_tournaments'] = Tournament.objects.filter(status='upcoming')
        return context


class TournamentDetailView(DetailView):
    """Tournament detail page with all matches."""
    model = Tournament
    template_name = 'frontend/tournaments/detail.html'
    context_object_name = 'tournament'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        context['matches'] = tournament.matches.select_related(
            'home_team', 'away_team'
        ).order_by('-match_date', '-match_time')
        context['completed_matches'] = tournament.matches.filter(
            status='completed'
        ).select_related('home_team', 'away_team').order_by('-match_date')
        context['upcoming_matches'] = tournament.matches.filter(
            status='scheduled'
        ).select_related('home_team', 'away_team').order_by('match_date')
        return context
