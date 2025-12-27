"""
Facilities Admin Views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import Facility, FacilityCategory
from .forms import FacilityForm, FacilityCategoryForm


class FacilityListView(AdminRequiredMixin, ListView):
    """List all facilities."""
    model = Facility
    template_name = 'admin_dashboard/facilities/list.html'
    context_object_name = 'facilities'
    paginate_by = 12

    def get_queryset(self):
        return Facility.objects.select_related('category').order_by('display_order', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FacilityCategory.objects.filter(is_active=True)
        return context


class FacilityCreateView(AdminRequiredMixin, CreateView):
    """Create a new facility."""
    model = Facility
    form_class = FacilityForm
    template_name = 'admin_dashboard/facilities/form.html'
    success_url = reverse_lazy('admin_dashboard:facilities:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FacilityCategory.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Facility created successfully.')
        return super().form_valid(form)


class FacilityUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing facility."""
    model = Facility
    form_class = FacilityForm
    template_name = 'admin_dashboard/facilities/form.html'
    success_url = reverse_lazy('admin_dashboard:facilities:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FacilityCategory.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Facility updated successfully.')
        return super().form_valid(form)


class FacilityDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a facility."""
    model = Facility
    template_name = 'admin_dashboard/facilities/delete.html'
    success_url = reverse_lazy('admin_dashboard:facilities:list')

    def form_valid(self, form):
        messages.success(self.request, 'Facility deleted successfully.')
        return super().form_valid(form)


# Category Views
class CategoryListView(AdminRequiredMixin, ListView):
    """List all facility categories."""
    model = FacilityCategory
    template_name = 'admin_dashboard/facilities/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Create a new category."""
    model = FacilityCategory
    form_class = FacilityCategoryForm
    template_name = 'admin_dashboard/facilities/category_form.html'
    success_url = reverse_lazy('admin_dashboard:facilities:category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully.')
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Update a category."""
    model = FacilityCategory
    form_class = FacilityCategoryForm
    template_name = 'admin_dashboard/facilities/category_form.html'
    success_url = reverse_lazy('admin_dashboard:facilities:category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully.')
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a category."""
    model = FacilityCategory
    template_name = 'admin_dashboard/facilities/category_delete.html'
    success_url = reverse_lazy('admin_dashboard:facilities:category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category deleted successfully.')
        return super().form_valid(form)
