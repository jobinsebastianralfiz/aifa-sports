"""
Frontend URLs - Public website pages.
"""

from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('community/', views.CommunityView.as_view(), name='community'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    # API endpoints
    path('api/chatbot/', views.ChatbotAPIView.as_view(), name='chatbot_api'),
]
