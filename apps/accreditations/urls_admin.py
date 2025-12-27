from django.urls import path
from . import views_admin

urlpatterns = [
    path('', views_admin.AccreditationListView.as_view(), name='list'),
    path('add/', views_admin.AccreditationCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.AccreditationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.AccreditationDeleteView.as_view(), name='delete'),
]
