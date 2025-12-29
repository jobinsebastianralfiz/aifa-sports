"""
Tournaments app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'tournaments_admin'

urlpatterns = [
    path('', views_admin.TournamentListView.as_view(), name='list'),
    path('add/', views_admin.TournamentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.TournamentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.TournamentDeleteView.as_view(), name='delete'),
]
