"""
Blog app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from apps.accounts.decorators import AdminRequiredMixin
from .models import BlogPost, BlogCategory
from .forms import BlogPostForm, BlogCategoryForm


# Category Views
class CategoryListView(AdminRequiredMixin, ListView):
    """Admin blog category listing."""
    model = BlogCategory
    template_name = 'admin_dashboard/blog/categories/list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        return BlogCategory.objects.all().order_by('name')


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Create blog category."""
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'admin_dashboard/blog/categories/form.html'
    success_url = reverse_lazy('admin_dashboard:blog:category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Update blog category."""
    model = BlogCategory
    form_class = BlogCategoryForm
    template_name = 'admin_dashboard/blog/categories/form.html'
    success_url = reverse_lazy('admin_dashboard:blog:category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete blog category."""
    model = BlogCategory
    template_name = 'admin_dashboard/blog/categories/delete.html'
    success_url = reverse_lazy('admin_dashboard:blog:category-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Post Views
class PostListView(AdminRequiredMixin, ListView):
    """Admin blog post listing."""
    model = BlogPost
    template_name = 'admin_dashboard/blog/posts/list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = BlogPost.objects.select_related('category', 'author').order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = BlogPost.Status.choices
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class PostCreateView(AdminRequiredMixin, CreateView):
    """Create blog post."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'admin_dashboard/blog/posts/form.html'
    success_url = reverse_lazy('admin_dashboard:blog:post-list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
        post.save()
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)


class PostUpdateView(AdminRequiredMixin, UpdateView):
    """Update blog post."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'admin_dashboard/blog/posts/form.html'
    success_url = reverse_lazy('admin_dashboard:blog:post-list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
        post.save()
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(AdminRequiredMixin, DeleteView):
    """Delete blog post."""
    model = BlogPost
    template_name = 'admin_dashboard/blog/posts/delete.html'
    success_url = reverse_lazy('admin_dashboard:blog:post-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Blog post deleted successfully!')
        return super().delete(request, *args, **kwargs)
