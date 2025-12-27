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

    # Legal pages
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('terms-conditions/', views.TermsConditionsView.as_view(), name='terms'),
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),

    # API endpoints
    path('api/chatbot/', views.ChatbotAPIView.as_view(), name='chatbot_api'),
]
