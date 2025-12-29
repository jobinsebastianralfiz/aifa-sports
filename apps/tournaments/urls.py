"""
Tournaments app frontend URLs.
"""

from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.TournamentListView.as_view(), name='list'),
    path('<slug:slug>/', views.TournamentDetailView.as_view(), name='detail'),
]
