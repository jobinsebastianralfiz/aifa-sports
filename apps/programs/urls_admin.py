"""
Programs app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'programs_admin'

urlpatterns = [
    path('', views_admin.ProgramListView.as_view(), name='list'),
    path('add/', views_admin.ProgramCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.ProgramUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.ProgramDeleteView.as_view(), name='delete'),
]
