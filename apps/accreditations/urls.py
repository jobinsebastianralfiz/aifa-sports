from django.urls import path
from . import views

app_name = 'accreditations'

urlpatterns = [
    path('', views.AccreditationListView.as_view(), name='list'),
]
