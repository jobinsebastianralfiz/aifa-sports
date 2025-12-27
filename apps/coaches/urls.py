"""
Coaches app frontend URLs.
"""

from django.urls import path
from . import views

app_name = 'coaches'

urlpatterns = [
    path('', views.CoachListView.as_view(), name='list'),
    path('<slug:slug>/', views.CoachDetailView.as_view(), name='detail'),
]
