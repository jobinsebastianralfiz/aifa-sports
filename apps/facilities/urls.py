"""
Facilities Frontend URLs.
"""

from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    path('', views.FacilityListView.as_view(), name='list'),
    path('<slug:slug>/', views.FacilityDetailView.as_view(), name='detail'),
]
