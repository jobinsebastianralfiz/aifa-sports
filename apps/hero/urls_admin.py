"""
Hero slides app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'hero_admin'

urlpatterns = [
    path('', views_admin.HeroSlideListView.as_view(), name='list'),
    path('add/', views_admin.HeroSlideCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.HeroSlideUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.HeroSlideDeleteView.as_view(), name='delete'),
]
