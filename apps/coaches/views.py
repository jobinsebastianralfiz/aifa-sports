"""
Coaches app frontend views.
"""

from django.views.generic import ListView, DetailView
from .models import Coach


class CoachListView(ListView):
    """Public coach listing."""
    model = Coach
    template_name = 'frontend/coaches/list.html'
    context_object_name = 'coaches'
    paginate_by = 12

    def get_queryset(self):
        return Coach.objects.filter(
            status='active',
            show_on_website=True
        ).order_by('display_order', 'first_name')


class CoachDetailView(DetailView):
    """Public coach profile page."""
    model = Coach
    template_name = 'frontend/coaches/detail.html'
    context_object_name = 'coach'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Coach.objects.filter(status='active', show_on_website=True)
