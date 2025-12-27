"""
Facilities Frontend Views.
"""

from django.views.generic import ListView, DetailView
from .models import Facility, FacilityCategory


class FacilityListView(ListView):
    """List all active facilities."""
    model = Facility
    template_name = 'frontend/facilities/list.html'
    context_object_name = 'facilities'

    def get_queryset(self):
        return Facility.objects.filter(is_active=True).select_related('category').order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FacilityCategory.objects.filter(is_active=True).prefetch_related('facilities')
        return context


class FacilityDetailView(DetailView):
    """Show facility details."""
    model = Facility
    template_name = 'frontend/facilities/detail.html'
    context_object_name = 'facility'

    def get_queryset(self):
        return Facility.objects.filter(is_active=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_facilities'] = Facility.objects.filter(
            is_active=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context
