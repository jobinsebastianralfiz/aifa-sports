"""
Gallery app admin dashboard views.
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin
from .models import GalleryCategory, GalleryImage, GalleryVideo
from .forms import GalleryCategoryForm, GalleryImageForm, GalleryVideoForm


# Category Views
class CategoryListView(AdminRequiredMixin, ListView):
    """Admin gallery category listing."""
    model = GalleryCategory
    template_name = 'admin_dashboard/gallery/list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        return GalleryCategory.objects.all().order_by('display_order', 'name')


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Create gallery category."""
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'admin_dashboard/gallery/album_form.html'
    success_url = reverse_lazy('admin_dashboard:gallery:image-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Update gallery category."""
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'admin_dashboard/gallery/album_form.html'
    success_url = reverse_lazy('admin_dashboard:gallery:image-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete gallery category."""
    model = GalleryCategory
    template_name = 'admin_dashboard/gallery/delete.html'
    success_url = reverse_lazy('admin_dashboard:gallery:image-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Image Views
class ImageListView(AdminRequiredMixin, ListView):
    """Admin gallery image listing."""
    model = GalleryImage
    template_name = 'admin_dashboard/gallery/list.html'
    context_object_name = 'images'
    paginate_by = 24

    def get_queryset(self):
        queryset = GalleryImage.objects.select_related('category').order_by('-created_at')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryCategory.objects.all().order_by('name')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class ImageCreateView(AdminRequiredMixin, CreateView):
    """Upload gallery image."""
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'admin_dashboard/gallery/form.html'
    success_url = reverse_lazy('admin_dashboard:gallery:image-list')

    def form_valid(self, form):
        messages.success(self.request, 'Image uploaded successfully!')
        return super().form_valid(form)


class ImageUpdateView(AdminRequiredMixin, UpdateView):
    """Update gallery image."""
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'admin_dashboard/gallery/form.html'
    success_url = reverse_lazy('admin_dashboard:gallery:image-list')

    def form_valid(self, form):
        messages.success(self.request, 'Image updated successfully!')
        return super().form_valid(form)


class ImageDeleteView(AdminRequiredMixin, DeleteView):
    """Delete gallery image."""
    model = GalleryImage
    template_name = 'admin_dashboard/gallery/delete.html'
    success_url = reverse_lazy('admin_dashboard:gallery:image-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Image deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Video Views
class VideoListView(AdminRequiredMixin, ListView):
    """Admin gallery video listing."""
    model = GalleryVideo
    template_name = 'admin_dashboard/gallery/video_list.html'
    context_object_name = 'videos'
    paginate_by = 24

    def get_queryset(self):
        queryset = GalleryVideo.objects.order_by('-created_at')
        platform = self.request.GET.get('platform')
        if platform:
            queryset = queryset.filter(platform=platform)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = GalleryVideo.Platform.choices
        context['selected_platform'] = self.request.GET.get('platform', '')
        return context


class VideoCreateView(AdminRequiredMixin, CreateView):
    """Add gallery video."""
    model = GalleryVideo
    form_class = GalleryVideoForm
    template_name = 'admin_dashboard/gallery/video_form.html'
    success_url = reverse_lazy('admin_dashboard:gallery:video-list')

    def form_valid(self, form):
        messages.success(self.request, 'Video added successfully!')
        return super().form_valid(form)


class VideoUpdateView(AdminRequiredMixin, UpdateView):
    """Update gallery video."""
    model = GalleryVideo
    form_class = GalleryVideoForm
    template_name = 'admin_dashboard/gallery/video_form.html'
    success_url = reverse_lazy('admin_dashboard:gallery:video-list')

    def form_valid(self, form):
        messages.success(self.request, 'Video updated successfully!')
        return super().form_valid(form)


class VideoDeleteView(AdminRequiredMixin, DeleteView):
    """Delete gallery video."""
    model = GalleryVideo
    template_name = 'admin_dashboard/gallery/video_delete.html'
    success_url = reverse_lazy('admin_dashboard:gallery:video-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Video deleted successfully!')
        return super().delete(request, *args, **kwargs)
