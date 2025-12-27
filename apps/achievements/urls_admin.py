from django.urls import path
from . import views_admin

urlpatterns = [
    path('', views_admin.AchievementListView.as_view(), name='list'),
    path('add/', views_admin.AchievementCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views_admin.AchievementUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views_admin.AchievementDeleteView.as_view(), name='delete'),
]
