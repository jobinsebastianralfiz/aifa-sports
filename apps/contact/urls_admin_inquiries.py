"""
Inquiries admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'inquiries_admin'

urlpatterns = [
    path('', views_admin.InquiryListView.as_view(), name='list'),
    path('<int:pk>/', views_admin.InquiryDetailView.as_view(), name='detail'),
    path('<int:pk>/update-status/', views_admin.InquiryUpdateStatusView.as_view(), name='update_status'),
]
