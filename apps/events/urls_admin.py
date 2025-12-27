"""
Events app admin URLs.
"""

from django.urls import path
from . import views_admin

app_name = 'events_admin'

urlpatterns = [
    path('', views_admin.EventListView.as_view(), name='list'),
    path('add/', views_admin.EventCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.EventUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/form-builder/', views_admin.FormBuilderView.as_view(), name='form-builder'),
    path('<int:pk>/form-builder/add-field/', views_admin.AddFormFieldView.as_view(), name='add-form-field'),
    path('<int:pk>/form-builder/delete-field/<int:field_id>/', views_admin.DeleteFormFieldView.as_view(), name='delete-form-field'),
    path('<int:pk>/form-builder/reorder/', views_admin.ReorderFormFieldsView.as_view(), name='reorder-form-fields'),
    path('<int:event_pk>/registrations/', views_admin.RegistrationListView.as_view(), name='registrations'),
    path('<int:event_pk>/registrations/export/', views_admin.ExportRegistrationsView.as_view(), name='export-registrations'),
    path('registration/<int:pk>/', views_admin.RegistrationDetailView.as_view(), name='registration-detail'),
    path('registration/<int:pk>/status/', views_admin.RegistrationUpdateStatusView.as_view(), name='registration-status'),
    path('registration/<int:pk>/delete/', views_admin.RegistrationDeleteView.as_view(), name='registration-delete'),
]
