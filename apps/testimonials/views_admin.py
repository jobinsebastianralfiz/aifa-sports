"""
Testimonials app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import Testimonial
from .forms import TestimonialForm


class TestimonialListView(AdminRequiredMixin, ListView):
    """Admin testimonial listing."""
    model = Testimonial
    template_name = 'admin_dashboard/testimonials/list.html'
    context_object_name = 'testimonials'
    paginate_by = 20

    def get_queryset(self):
        return Testimonial.objects.all().order_by('-created_at')


class TestimonialCreateView(AdminRequiredMixin, CreateView):
    """Create testimonial."""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'admin_dashboard/testimonials/form.html'
    success_url = reverse_lazy('admin_dashboard:testimonials:list')

    def form_valid(self, form):
        messages.success(self.request, 'Testimonial created successfully!')
        return super().form_valid(form)


class TestimonialUpdateView(AdminRequiredMixin, UpdateView):
    """Update testimonial."""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'admin_dashboard/testimonials/form.html'
    success_url = reverse_lazy('admin_dashboard:testimonials:list')

    def form_valid(self, form):
        messages.success(self.request, 'Testimonial updated successfully!')
        return super().form_valid(form)


class TestimonialDeleteView(AdminRequiredMixin, DeleteView):
    """Delete testimonial."""
    model = Testimonial
    template_name = 'admin_dashboard/testimonials/delete.html'
    success_url = reverse_lazy('admin_dashboard:testimonials:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Testimonial deleted successfully!')
        return super().delete(request, *args, **kwargs)
