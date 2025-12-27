"""
News app frontend views.
"""

from django.views.generic import ListView, DetailView
from .models import News


class NewsListView(ListView):
    """Public news listing."""
    model = News
    template_name = 'frontend/news/list.html'
    context_object_name = 'news_list'
    paginate_by = 12

    def get_queryset(self):
        return News.objects.filter(status='published').order_by('-published_at')


class NewsDetailView(DetailView):
    """Public news detail page."""
    model = News
    template_name = 'frontend/news/detail.html'
    context_object_name = 'news'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return News.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.objects.filter(
            status='published'
        ).exclude(pk=self.object.pk)[:3]
        return context
