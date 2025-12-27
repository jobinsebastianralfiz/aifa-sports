"""
Contact messages admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'messages_admin'

urlpatterns = [
    path('', views_admin.MessageListView.as_view(), name='list'),
    path('<int:pk>/', views_admin.MessageDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views_admin.MessageDeleteView.as_view(), name='delete'),
]
