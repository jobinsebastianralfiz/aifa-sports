"""
Blog app frontend views.
"""

from django.views.generic import ListView, DetailView
from .models import BlogPost, BlogCategory


class BlogListView(ListView):
    """Public blog listing."""
    model = BlogPost
    template_name = 'frontend/blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').order_by('-published_at')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_active=True)
        context['selected_category'] = self.kwargs.get('category_slug', '')
        return context


class BlogDetailView(DetailView):
    """Public blog post detail page."""
    model = BlogPost
    template_name = 'frontend/blog/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = BlogPost.objects.filter(
            status='published',
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context
