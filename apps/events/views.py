"""
Events app frontend views.
"""

from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Event, EventFormField, EventRegistration


class EventListView(ListView):
    """Public event listing."""
    model = Event
    template_name = 'frontend/events/list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = Event.objects.filter(status__in=['upcoming', 'ongoing'])
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.EventType.choices
        context['selected_type'] = self.request.GET.get('type', '')
        return context


class EventDetailView(DetailView):
    """Public event detail page."""
    model = Event
    template_name = 'frontend/events/detail.html'
    context_object_name = 'event'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Event.objects.exclude(status='draft')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_fields'] = EventFormField.objects.filter(
            event=self.object
        ).order_by('display_order')
        context['can_register'] = self.object.is_registration_open
        return context


class EventRegisterView(FormView):
    """Event registration with dynamic form."""
    template_name = 'frontend/events/register.html'

    def get_event(self):
        return get_object_or_404(
            Event.objects.filter(status__in=['upcoming', 'ongoing'], registration_required=True),
            slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_event()
        context['form_fields'] = EventFormField.objects.filter(
            event=context['event']
        ).order_by('display_order')
        return context

    def get_form(self, form_class=None):
        from django import forms

        event = self.get_event()
        form_fields = EventFormField.objects.filter(event=event).order_by('display_order')

        class DynamicForm(forms.Form):
            pass

        for field in form_fields:
            field_kwargs = {
                'label': field.label,
                'required': field.is_required,
                'help_text': field.help_text or '',
            }

            if field.field_type == 'text':
                DynamicForm.base_fields[field.field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={'class': 'form-input'}),
                    **field_kwargs
                )
            elif field.field_type == 'email':
                DynamicForm.base_fields[field.field_name] = forms.EmailField(
                    widget=forms.EmailInput(attrs={'class': 'form-input'}),
                    **field_kwargs
                )
            elif field.field_type == 'phone':
                DynamicForm.base_fields[field.field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'tel'}),
                    **field_kwargs
                )
            elif field.field_type == 'number':
                DynamicForm.base_fields[field.field_name] = forms.IntegerField(
                    widget=forms.NumberInput(attrs={'class': 'form-input'}),
                    **field_kwargs
                )
            elif field.field_type == 'date':
                DynamicForm.base_fields[field.field_name] = forms.DateField(
                    widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
                    **field_kwargs
                )
            elif field.field_type == 'textarea':
                DynamicForm.base_fields[field.field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
                    **field_kwargs
                )
            elif field.field_type == 'select':
                choices = [(opt, opt) for opt in field.options]
                DynamicForm.base_fields[field.field_name] = forms.ChoiceField(
                    widget=forms.Select(attrs={'class': 'form-select'}),
                    choices=[('', '-- Select --')] + choices,
                    **field_kwargs
                )
            elif field.field_type == 'radio':
                choices = [(opt, opt) for opt in field.options]
                DynamicForm.base_fields[field.field_name] = forms.ChoiceField(
                    widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
                    choices=choices,
                    **field_kwargs
                )
            elif field.field_type == 'checkbox':
                DynamicForm.base_fields[field.field_name] = forms.BooleanField(
                    widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
                    **field_kwargs
                )

        if self.request.method == 'POST':
            return DynamicForm(self.request.POST)
        return DynamicForm()

    def form_valid(self, form):
        event = self.get_event()

        # Check capacity
        if not event.is_registration_open:
            messages.error(self.request, 'Sorry, registration is closed for this event.')
            return self.form_invalid(form)

        # Extract common fields from form data if they exist
        form_data = form.cleaned_data
        participant_name = form_data.get('full_name', '') or form_data.get('name', '') or 'Participant'
        email = form_data.get('email', '') or 'no-email@example.com'
        phone = form_data.get('phone', '') or form_data.get('phone_number', '') or ''

        # Save registration
        EventRegistration.objects.create(
            event=event,
            participant_name=participant_name,
            email=email,
            phone=phone,
            form_data=form_data,
            status='pending'
        )

        messages.success(
            self.request,
            'Registration successful! We will contact you with further details.'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('events:detail', kwargs={'slug': self.kwargs['slug']})
