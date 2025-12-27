"""
Gallery app frontend URLs.
"""

from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='list'),
    path('<slug:slug>/', views.GalleryCategoryView.as_view(), name='category'),
]
