from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.accounts.decorators import AdminRequiredMixin
from .models import Achievement
from .forms import AchievementForm


class AchievementListView(AdminRequiredMixin, ListView):
    model = Achievement
    template_name = 'admin_dashboard/achievements/list.html'
    context_object_name = 'achievements'
    paginate_by = 20

    def get_queryset(self):
        return Achievement.objects.all().order_by('display_order', '-year')


class AchievementCreateView(AdminRequiredMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'admin_dashboard/achievements/form.html'
    success_url = reverse_lazy('admin_dashboard:achievements:list')

    def form_valid(self, form):
        messages.success(self.request, 'Achievement created successfully!')
        return super().form_valid(form)


class AchievementUpdateView(AdminRequiredMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'admin_dashboard/achievements/form.html'
    success_url = reverse_lazy('admin_dashboard:achievements:list')

    def form_valid(self, form):
        messages.success(self.request, 'Achievement updated successfully!')
        return super().form_valid(form)


class AchievementDeleteView(AdminRequiredMixin, DeleteView):
    model = Achievement
    template_name = 'admin_dashboard/achievements/delete.html'
    success_url = reverse_lazy('admin_dashboard:achievements:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Achievement deleted successfully!')
        return super().delete(request, *args, **kwargs)
