"""
Matches admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'matches_admin'

urlpatterns = [
    path('', views_admin.MatchListView.as_view(), name='list'),
    path('add/', views_admin.MatchCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.MatchUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.MatchDeleteView.as_view(), name='delete'),
]
