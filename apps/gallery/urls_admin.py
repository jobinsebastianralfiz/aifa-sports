"""
Gallery app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'gallery_admin'

urlpatterns = [
    # Images
    path('', views_admin.ImageListView.as_view(), name='image-list'),
    path('add/', views_admin.ImageCreateView.as_view(), name='image-create'),
    path('<int:pk>/edit/', views_admin.ImageUpdateView.as_view(), name='image-update'),
    path('<int:pk>/delete/', views_admin.ImageDeleteView.as_view(), name='image-delete'),
    # Categories
    path('categories/', views_admin.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views_admin.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views_admin.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views_admin.CategoryDeleteView.as_view(), name='category-delete'),
    # Videos
    path('videos/', views_admin.VideoListView.as_view(), name='video-list'),
    path('videos/add/', views_admin.VideoCreateView.as_view(), name='video-create'),
    path('videos/<int:pk>/edit/', views_admin.VideoUpdateView.as_view(), name='video-update'),
    path('videos/<int:pk>/delete/', views_admin.VideoDeleteView.as_view(), name='video-delete'),
]
