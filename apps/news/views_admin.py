"""
News app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from apps.accounts.decorators import AdminRequiredMixin
from .models import News
from .forms import NewsForm


class NewsListView(AdminRequiredMixin, ListView):
    """Admin news listing."""
    model = News
    template_name = 'admin_dashboard/news/list.html'
    context_object_name = 'news_list'
    paginate_by = 20

    def get_queryset(self):
        return News.objects.all().order_by('-created_at')


class NewsCreateView(AdminRequiredMixin, CreateView):
    """Create news article."""
    model = News
    form_class = NewsForm
    template_name = 'admin_dashboard/news/form.html'
    success_url = reverse_lazy('admin_dashboard:news:list')

    def form_valid(self, form):
        news = form.save(commit=False)
        if news.status == 'published' and not news.published_at:
            news.published_at = timezone.now()
        news.save()
        messages.success(self.request, 'News article created successfully!')
        return super().form_valid(form)


class NewsUpdateView(AdminRequiredMixin, UpdateView):
    """Update news article."""
    model = News
    form_class = NewsForm
    template_name = 'admin_dashboard/news/form.html'
    success_url = reverse_lazy('admin_dashboard:news:list')

    def form_valid(self, form):
        news = form.save(commit=False)
        if news.status == 'published' and not news.published_at:
            news.published_at = timezone.now()
        news.save()
        messages.success(self.request, 'News article updated successfully!')
        return super().form_valid(form)


class NewsDeleteView(AdminRequiredMixin, DeleteView):
    """Delete news article."""
    model = News
    template_name = 'admin_dashboard/news/delete.html'
    success_url = reverse_lazy('admin_dashboard:news:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'News article deleted successfully!')
        return super().delete(request, *args, **kwargs)
