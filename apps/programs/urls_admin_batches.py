"""
Batches admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'batches_admin'

urlpatterns = [
    path('', views_admin.BatchListView.as_view(), name='list'),
    path('add/', views_admin.BatchCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.BatchUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.BatchDeleteView.as_view(), name='delete'),
]
