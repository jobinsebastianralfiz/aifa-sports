"""
Tournaments app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import Tournament, Team, Match
from .forms import TournamentForm, TeamForm, MatchForm


# Tournament Views
class TournamentListView(AdminRequiredMixin, ListView):
    """Admin tournament listing."""
    model = Tournament
    template_name = 'admin_dashboard/tournaments/list.html'
    context_object_name = 'tournaments'
    paginate_by = 20

    def get_queryset(self):
        return Tournament.objects.all().order_by('-start_date')


class TournamentCreateView(AdminRequiredMixin, CreateView):
    """Create new tournament."""
    model = Tournament
    form_class = TournamentForm
    template_name = 'admin_dashboard/tournaments/form.html'
    success_url = reverse_lazy('admin_dashboard:tournaments:list')

    def form_valid(self, form):
        messages.success(self.request, 'Tournament created successfully!')
        return super().form_valid(form)


class TournamentUpdateView(AdminRequiredMixin, UpdateView):
    """Update tournament."""
    model = Tournament
    form_class = TournamentForm
    template_name = 'admin_dashboard/tournaments/form.html'
    success_url = reverse_lazy('admin_dashboard:tournaments:list')

    def form_valid(self, form):
        messages.success(self.request, 'Tournament updated successfully!')
        return super().form_valid(form)


class TournamentDeleteView(AdminRequiredMixin, DeleteView):
    """Delete tournament."""
    model = Tournament
    template_name = 'admin_dashboard/tournaments/delete.html'
    success_url = reverse_lazy('admin_dashboard:tournaments:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tournament deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Team Views
class TeamListView(AdminRequiredMixin, ListView):
    """Admin team listing."""
    model = Team
    template_name = 'admin_dashboard/tournaments/teams/list.html'
    context_object_name = 'teams'
    paginate_by = 20

    def get_queryset(self):
        return Team.objects.all().order_by('name')


class TeamCreateView(AdminRequiredMixin, CreateView):
    """Create new team."""
    model = Team
    form_class = TeamForm
    template_name = 'admin_dashboard/tournaments/teams/form.html'
    success_url = reverse_lazy('admin_dashboard:teams:list')

    def form_valid(self, form):
        messages.success(self.request, 'Team created successfully!')
        return super().form_valid(form)


class TeamUpdateView(AdminRequiredMixin, UpdateView):
    """Update team."""
    model = Team
    form_class = TeamForm
    template_name = 'admin_dashboard/tournaments/teams/form.html'
    success_url = reverse_lazy('admin_dashboard:teams:list')

    def form_valid(self, form):
        messages.success(self.request, 'Team updated successfully!')
        return super().form_valid(form)


class TeamDeleteView(AdminRequiredMixin, DeleteView):
    """Delete team."""
    model = Team
    template_name = 'admin_dashboard/tournaments/teams/delete.html'
    success_url = reverse_lazy('admin_dashboard:teams:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Team deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Match Views
class MatchListView(AdminRequiredMixin, ListView):
    """Admin match listing."""
    model = Match
    template_name = 'admin_dashboard/tournaments/matches/list.html'
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        return Match.objects.all().select_related('tournament', 'home_team', 'away_team').order_by('-match_date')


class MatchCreateView(AdminRequiredMixin, CreateView):
    """Create new match."""
    model = Match
    form_class = MatchForm
    template_name = 'admin_dashboard/tournaments/matches/form.html'
    success_url = reverse_lazy('admin_dashboard:matches:list')

    def form_valid(self, form):
        messages.success(self.request, 'Match created successfully!')
        return super().form_valid(form)


class MatchUpdateView(AdminRequiredMixin, UpdateView):
    """Update match."""
    model = Match
    form_class = MatchForm
    template_name = 'admin_dashboard/tournaments/matches/form.html'
    success_url = reverse_lazy('admin_dashboard:matches:list')

    def form_valid(self, form):
        messages.success(self.request, 'Match updated successfully!')
        return super().form_valid(form)


class MatchDeleteView(AdminRequiredMixin, DeleteView):
    """Delete match."""
    model = Match
    template_name = 'admin_dashboard/tournaments/matches/delete.html'
    success_url = reverse_lazy('admin_dashboard:matches:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Match deleted successfully!')
        return super().delete(request, *args, **kwargs)
