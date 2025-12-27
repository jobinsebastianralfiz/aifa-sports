"""
News app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'news_admin'

urlpatterns = [
    path('', views_admin.NewsListView.as_view(), name='list'),
    path('add/', views_admin.NewsCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.NewsDeleteView.as_view(), name='delete'),
]
