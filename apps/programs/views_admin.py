"""
Programs app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import Program, Batch
from .forms import ProgramForm, BatchForm


# Program Views
class ProgramListView(AdminRequiredMixin, ListView):
    """Admin program listing."""
    model = Program
    template_name = 'admin_dashboard/programs/list.html'
    context_object_name = 'programs'
    paginate_by = 20

    def get_queryset(self):
        return Program.objects.all().order_by('display_order', 'name')


class ProgramCreateView(AdminRequiredMixin, CreateView):
    """Create new program."""
    model = Program
    form_class = ProgramForm
    template_name = 'admin_dashboard/programs/form.html'
    success_url = reverse_lazy('admin_dashboard:programs:list')

    def form_valid(self, form):
        messages.success(self.request, 'Program created successfully!')
        return super().form_valid(form)


class ProgramUpdateView(AdminRequiredMixin, UpdateView):
    """Update program."""
    model = Program
    form_class = ProgramForm
    template_name = 'admin_dashboard/programs/form.html'
    success_url = reverse_lazy('admin_dashboard:programs:list')

    def form_valid(self, form):
        messages.success(self.request, 'Program updated successfully!')
        return super().form_valid(form)


class ProgramDeleteView(AdminRequiredMixin, DeleteView):
    """Delete program."""
    model = Program
    template_name = 'admin_dashboard/programs/delete.html'
    success_url = reverse_lazy('admin_dashboard:programs:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Program deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Batch Views
class BatchListView(AdminRequiredMixin, ListView):
    """Admin batch listing."""
    model = Batch
    template_name = 'admin_html/batches.html'
    context_object_name = 'batches'
    paginate_by = 20

    def get_queryset(self):
        return Batch.objects.select_related('program').order_by('program__name', 'name')


class BatchCreateView(AdminRequiredMixin, CreateView):
    """Create new batch."""
    model = Batch
    form_class = BatchForm
    template_name = 'admin_html/batch-detail.html'
    success_url = reverse_lazy('admin_dashboard:batches:list')

    def form_valid(self, form):
        messages.success(self.request, 'Batch created successfully!')
        return super().form_valid(form)


class BatchUpdateView(AdminRequiredMixin, UpdateView):
    """Update batch."""
    model = Batch
    form_class = BatchForm
    template_name = 'admin_html/batch-detail.html'
    success_url = reverse_lazy('admin_dashboard:batches:list')

    def form_valid(self, form):
        messages.success(self.request, 'Batch updated successfully!')
        return super().form_valid(form)


class BatchDeleteView(AdminRequiredMixin, DeleteView):
    """Delete batch."""
    model = Batch
    template_name = 'admin_html/batches.html'
    success_url = reverse_lazy('admin_dashboard:batches:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Batch deleted successfully!')
        return super().delete(request, *args, **kwargs)
