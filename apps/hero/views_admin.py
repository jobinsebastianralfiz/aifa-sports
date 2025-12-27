"""
Hero app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import HeroSlide
from .forms import HeroSlideForm


class HeroSlideListView(AdminRequiredMixin, ListView):
    """Admin hero slide listing."""
    model = HeroSlide
    template_name = 'admin_dashboard/hero/list.html'
    context_object_name = 'slides'
    paginate_by = 20

    def get_queryset(self):
        return HeroSlide.objects.all().order_by('display_order')


class HeroSlideCreateView(AdminRequiredMixin, CreateView):
    """Create hero slide."""
    model = HeroSlide
    form_class = HeroSlideForm
    template_name = 'admin_dashboard/hero/form.html'
    success_url = reverse_lazy('admin_dashboard:hero:list')

    def form_valid(self, form):
        messages.success(self.request, 'Hero slide created successfully!')
        return super().form_valid(form)


class HeroSlideUpdateView(AdminRequiredMixin, UpdateView):
    """Update hero slide."""
    model = HeroSlide
    form_class = HeroSlideForm
    template_name = 'admin_dashboard/hero/form.html'
    success_url = reverse_lazy('admin_dashboard:hero:list')

    def form_valid(self, form):
        messages.success(self.request, 'Hero slide updated successfully!')
        return super().form_valid(form)


class HeroSlideDeleteView(AdminRequiredMixin, DeleteView):
    """Delete hero slide."""
    model = HeroSlide
    success_url = reverse_lazy('admin_dashboard:hero:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Hero slide deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle POST request for deletion."""
        messages.success(request, 'Hero slide deleted successfully!')
        return self.delete(request, *args, **kwargs)
