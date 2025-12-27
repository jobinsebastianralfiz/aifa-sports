"""
Gallery app frontend views.
"""

from django.views.generic import ListView, DetailView
from .models import GalleryCategory, GalleryImage, GalleryVideo


class GalleryListView(ListView):
    """Public gallery listing - shows categories."""
    model = GalleryCategory
    template_name = 'frontend/gallery/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return GalleryCategory.objects.filter(is_active=True).order_by('display_order', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Also get recent images for homepage display
        context['recent_images'] = GalleryImage.objects.filter(
            is_active=True
        ).select_related('category').order_by('-created_at')[:12]
        # Get videos for the videos tab
        context['videos'] = GalleryVideo.objects.filter(
            is_active=True
        ).order_by('display_order', '-created_at')
        context['featured_videos'] = GalleryVideo.objects.filter(
            is_active=True, is_featured=True
        ).order_by('display_order', '-created_at')[:4]
        return context


class GalleryCategoryView(DetailView):
    """Gallery category with images."""
    model = GalleryCategory
    template_name = 'frontend/gallery/category.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return GalleryCategory.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = GalleryImage.objects.filter(
            category=self.object,
            is_active=True
        ).order_by('display_order', '-created_at')
        context['categories'] = GalleryCategory.objects.filter(
            is_active=True
        ).order_by('display_order', 'name')
        return context
