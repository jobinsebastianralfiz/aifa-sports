"""
Contact app admin dashboard views.
"""

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from apps.accounts.decorators import AdminRequiredMixin
from .models import ContactMessage, Inquiry


# Contact Message Views
class MessageListView(AdminRequiredMixin, ListView):
    """Admin contact message listing."""
    model = ContactMessage
    template_name = 'admin_dashboard/messages/list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        queryset = ContactMessage.objects.all().order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ContactMessage.Status.choices
        context['selected_status'] = self.request.GET.get('status', '')
        context['new_count'] = ContactMessage.objects.filter(status='new').count()
        return context


class MessageDetailView(AdminRequiredMixin, DetailView):
    """View contact message details."""
    model = ContactMessage
    template_name = 'admin_dashboard/messages/detail.html'
    context_object_name = 'message'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Mark as read when viewed
        if obj.status == 'new':
            obj.status = 'read'
            obj.save(update_fields=['status'])
        return obj


class MessageUpdateStatusView(AdminRequiredMixin, View):
    """Update message status."""

    def post(self, request, pk):
        message = get_object_or_404(ContactMessage, pk=pk)
        status = request.POST.get('status')
        if status in dict(ContactMessage.Status.choices):
            message.status = status
            message.save(update_fields=['status'])
            messages.success(request, f'Message status updated to {status}.')
        return redirect('admin_dashboard:messages:detail', pk=pk)


class MessageDeleteView(AdminRequiredMixin, DeleteView):
    """Delete contact message."""
    model = ContactMessage
    template_name = 'admin_dashboard/messages/delete.html'
    success_url = reverse_lazy('admin_dashboard:messages:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Message deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Inquiry Views
class InquiryListView(AdminRequiredMixin, ListView):
    """Admin inquiry listing."""
    model = Inquiry
    template_name = 'admin_html/messages.html'
    context_object_name = 'inquiries'
    paginate_by = 20

    def get_queryset(self):
        queryset = Inquiry.objects.select_related('program').order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Inquiry.Status.choices
        context['selected_status'] = self.request.GET.get('status', '')
        context['new_count'] = Inquiry.objects.filter(status='new').count()
        return context


class InquiryDetailView(AdminRequiredMixin, DetailView):
    """View inquiry details."""
    model = Inquiry
    template_name = 'admin_html/messages.html'
    context_object_name = 'inquiry'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Mark as read when viewed
        if obj.status == 'new':
            obj.status = 'read'
            obj.save(update_fields=['status'])
        return obj


class InquiryUpdateStatusView(AdminRequiredMixin, View):
    """Update inquiry status."""

    def post(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        status = request.POST.get('status')
        if status in dict(Inquiry.Status.choices):
            inquiry.status = status
            inquiry.save(update_fields=['status'])
            messages.success(request, f'Inquiry status updated to {status}.')
        return redirect('admin_dashboard:inquiries:detail', pk=pk)


class InquiryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete inquiry."""
    model = Inquiry
    template_name = 'admin_html/messages.html'
    success_url = reverse_lazy('admin_dashboard:inquiries:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Inquiry deleted successfully!')
        return super().delete(request, *args, **kwargs)
