from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.accounts.decorators import AdminRequiredMixin
from .models import Accreditation
from .forms import AccreditationForm


class AccreditationListView(AdminRequiredMixin, ListView):
    model = Accreditation
    template_name = 'admin_dashboard/accreditations/list.html'
    context_object_name = 'accreditations'
    paginate_by = 20

    def get_queryset(self):
        return Accreditation.objects.all().order_by('display_order')


class AccreditationCreateView(AdminRequiredMixin, CreateView):
    model = Accreditation
    form_class = AccreditationForm
    template_name = 'admin_dashboard/accreditations/form.html'
    success_url = reverse_lazy('admin_dashboard:accreditations:list')

    def form_valid(self, form):
        messages.success(self.request, 'Accreditation created successfully!')
        return super().form_valid(form)


class AccreditationUpdateView(AdminRequiredMixin, UpdateView):
    model = Accreditation
    form_class = AccreditationForm
    template_name = 'admin_dashboard/accreditations/form.html'
    success_url = reverse_lazy('admin_dashboard:accreditations:list')

    def form_valid(self, form):
        messages.success(self.request, 'Accreditation updated successfully!')
        return super().form_valid(form)


class AccreditationDeleteView(AdminRequiredMixin, DeleteView):
    model = Accreditation
    template_name = 'admin_dashboard/accreditations/delete.html'
    success_url = reverse_lazy('admin_dashboard:accreditations:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Accreditation deleted successfully!')
        return super().delete(request, *args, **kwargs)
