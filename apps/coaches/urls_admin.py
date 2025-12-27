"""
Coaches app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'coaches_admin'

urlpatterns = [
    path('', views_admin.CoachListView.as_view(), name='list'),
    path('add/', views_admin.CoachCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.CoachUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.CoachDeleteView.as_view(), name='delete'),
]
