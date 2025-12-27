"""
Facilities Admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'facilities'

urlpatterns = [
    path('', views_admin.FacilityListView.as_view(), name='list'),
    path('add/', views_admin.FacilityCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.FacilityUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.FacilityDeleteView.as_view(), name='delete'),

    # Categories
    path('categories/', views_admin.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views_admin.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views_admin.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views_admin.CategoryDeleteView.as_view(), name='category-delete'),
]
