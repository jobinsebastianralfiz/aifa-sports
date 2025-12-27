"""
Blog app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'blog_admin'

urlpatterns = [
    # Posts
    path('', views_admin.PostListView.as_view(), name='post-list'),
    path('add/', views_admin.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/edit/', views_admin.PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', views_admin.PostDeleteView.as_view(), name='post-delete'),
    # Categories
    path('categories/', views_admin.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views_admin.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views_admin.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views_admin.CategoryDeleteView.as_view(), name='category-delete'),
]
