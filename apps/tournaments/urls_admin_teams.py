"""
Teams admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'teams_admin'

urlpatterns = [
    path('', views_admin.TeamListView.as_view(), name='list'),
    path('add/', views_admin.TeamCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.TeamUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.TeamDeleteView.as_view(), name='delete'),
]
