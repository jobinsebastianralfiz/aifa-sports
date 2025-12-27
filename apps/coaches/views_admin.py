"""
Coaches app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import Coach
from .forms import CoachForm


class CoachListView(AdminRequiredMixin, ListView):
    """Admin coach listing."""
    model = Coach
    template_name = 'admin_dashboard/coaches/list.html'
    context_object_name = 'coaches'
    paginate_by = 20

    def get_queryset(self):
        return Coach.objects.all().order_by('display_order', 'first_name')


class CoachCreateView(AdminRequiredMixin, CreateView):
    """Create new coach."""
    model = Coach
    form_class = CoachForm
    template_name = 'admin_dashboard/coaches/form.html'
    success_url = reverse_lazy('admin_dashboard:coaches:list')

    def form_valid(self, form):
        messages.success(self.request, 'Coach created successfully!')
        return super().form_valid(form)


class CoachUpdateView(AdminRequiredMixin, UpdateView):
    """Update coach."""
    model = Coach
    form_class = CoachForm
    template_name = 'admin_dashboard/coaches/form.html'
    success_url = reverse_lazy('admin_dashboard:coaches:list')

    def form_valid(self, form):
        messages.success(self.request, 'Coach updated successfully!')
        return super().form_valid(form)


class CoachDeleteView(AdminRequiredMixin, DeleteView):
    """Delete coach."""
    model = Coach
    template_name = 'admin_dashboard/coaches/delete.html'
    success_url = reverse_lazy('admin_dashboard:coaches:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Coach deleted successfully!')
        return super().delete(request, *args, **kwargs)
