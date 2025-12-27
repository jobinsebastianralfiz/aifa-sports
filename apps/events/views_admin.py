"""
Events app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
import csv

from apps.accounts.decorators import AdminRequiredMixin
from .models import Event, EventFormField, EventRegistration
from .forms import EventForm, EventFormFieldForm


# Event Views
class EventListView(AdminRequiredMixin, ListView):
    """Admin event listing."""
    model = Event
    template_name = 'admin_dashboard/events/list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        return Event.objects.all().order_by('-start_date')


class EventCreateView(AdminRequiredMixin, CreateView):
    """Create new event."""
    model = Event
    form_class = EventForm
    template_name = 'admin_dashboard/events/form.html'
    success_url = reverse_lazy('admin_dashboard:events:list')

    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)


class EventUpdateView(AdminRequiredMixin, UpdateView):
    """Update event."""
    model = Event
    form_class = EventForm
    template_name = 'admin_dashboard/events/form.html'
    success_url = reverse_lazy('admin_dashboard:events:list')

    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)


class EventDeleteView(AdminRequiredMixin, DeleteView):
    """Delete event."""
    model = Event
    template_name = 'admin_dashboard/events/delete.html'
    success_url = reverse_lazy('admin_dashboard:events:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Form Builder Views
class FormBuilderView(AdminRequiredMixin, DetailView):
    """Form builder for event registration."""
    model = Event
    template_name = 'admin_dashboard/events/form_builder.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_fields'] = EventFormField.objects.filter(
            event=self.object
        ).order_by('display_order')
        context['field_form'] = EventFormFieldForm()
        return context


class AddFormFieldView(AdminRequiredMixin, View):
    """Add field to event form."""

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = EventFormFieldForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.event = event
            # Set display_order to last
            last_field = EventFormField.objects.filter(event=event).order_by('-display_order').first()
            field.display_order = (last_field.display_order + 1) if last_field else 0
            field.save()
            messages.success(request, 'Field added successfully!')
        else:
            messages.error(request, 'Error adding field.')
        return redirect('admin_dashboard:events:form-builder', pk=pk)


class DeleteFormFieldView(AdminRequiredMixin, View):
    """Delete field from event form."""

    def post(self, request, pk, field_id):
        field = get_object_or_404(EventFormField, pk=field_id, event_id=pk)
        field.delete()
        messages.success(request, 'Field deleted successfully!')
        return redirect('admin_dashboard:events:form-builder', pk=pk)


class ReorderFormFieldsView(AdminRequiredMixin, View):
    """Reorder form fields via AJAX."""

    def post(self, request, pk):
        import json
        try:
            data = json.loads(request.body)
            for item in data.get('fields', []):
                EventFormField.objects.filter(
                    pk=item['id'],
                    event_id=pk
                ).update(display_order=item['order'])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Registration Views
class RegistrationListView(AdminRequiredMixin, ListView):
    """List all registrations for an event."""
    model = EventRegistration
    template_name = 'admin_dashboard/events/registrations/list.html'
    context_object_name = 'registrations'
    paginate_by = 50

    def get_queryset(self):
        self.event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        return EventRegistration.objects.filter(event=self.event).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        context['form_fields'] = EventFormField.objects.filter(event=self.event).order_by('display_order')
        return context


class RegistrationDetailView(AdminRequiredMixin, DetailView):
    """View registration details."""
    model = EventRegistration
    template_name = 'admin_dashboard/events/registrations/detail.html'
    context_object_name = 'registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object.event
        context['form_fields'] = EventFormField.objects.filter(
            event=self.object.event
        ).order_by('display_order')
        return context


class RegistrationDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a registration."""
    model = EventRegistration
    template_name = 'admin_dashboard/events/registrations/delete.html'
    context_object_name = 'registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object.event
        return context

    def get_success_url(self):
        return reverse('admin_dashboard:events:registrations', kwargs={'event_pk': self.object.event.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Registration deleted successfully!')
        return super().delete(request, *args, **kwargs)


class RegistrationUpdateStatusView(AdminRequiredMixin, View):
    """Update registration status."""

    def post(self, request, pk):
        registration = get_object_or_404(EventRegistration, pk=pk)
        status = request.POST.get('status')
        if status in dict(EventRegistration.Status.choices):
            registration.status = status
            registration.save(update_fields=['status'])
            messages.success(request, f'Registration status updated to {status}.')
        return redirect('admin_dashboard:events:registration-detail', pk=pk)


class ExportRegistrationsView(AdminRequiredMixin, View):
    """Export registrations to CSV."""

    def get(self, request, event_pk):
        event = get_object_or_404(Event, pk=event_pk)
        registrations = EventRegistration.objects.filter(event=event)
        form_fields = EventFormField.objects.filter(event=event).order_by('display_order')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{event.slug}-registrations.csv"'

        writer = csv.writer(response)

        # Header row
        headers = ['Registration ID', 'Status', 'Registered At']
        headers.extend([f.label for f in form_fields])
        writer.writerow(headers)

        # Data rows
        for reg in registrations:
            row = [reg.id, reg.status, reg.created_at.strftime('%Y-%m-%d %H:%M')]
            for field in form_fields:
                row.append(reg.form_data.get(field.field_name, ''))
            writer.writerow(row)

        return response
