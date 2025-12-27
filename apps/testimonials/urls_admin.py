"""
Testimonials app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'testimonials_admin'

urlpatterns = [
    path('', views_admin.TestimonialListView.as_view(), name='list'),
    path('add/', views_admin.TestimonialCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.TestimonialUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.TestimonialDeleteView.as_view(), name='delete'),
]
