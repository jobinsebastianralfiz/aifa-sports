"""
Admin Dashboard URLs.
"""

from django.urls import path, include
from . import views_admin

app_name = 'admin_dashboard'

# Page content URLs
page_content_patterns = [
    path('', views_admin.PageContentIndexView.as_view(), name='index'),
    path('page-settings/', views_admin.PageSettingsListView.as_view(), name='page-settings-list'),
    path('page-settings/add/', views_admin.PageSettingsCreateView.as_view(), name='page-settings-add'),
    path('page-settings/<int:pk>/edit/', views_admin.PageSettingsUpdateView.as_view(), name='page-settings-edit'),
    path('about/', views_admin.AboutContentView.as_view(), name='about-content'),
    path('homepage/', views_admin.HomepageContentView.as_view(), name='homepage-content'),
]

# Board Members URLs
board_members_patterns = [
    path('', views_admin.BoardMemberListView.as_view(), name='list'),
    path('add/', views_admin.BoardMemberCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views_admin.BoardMemberUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views_admin.BoardMemberDeleteView.as_view(), name='delete'),
]

# Community URLs
community_patterns = [
    path('', views_admin.CommunityActivityListView.as_view(), name='list'),
    path('add/', views_admin.CommunityActivityCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views_admin.CommunityActivityUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views_admin.CommunityActivityDeleteView.as_view(), name='delete'),
    path('page-content/', views_admin.CommunityPageContentView.as_view(), name='page-content'),
]

urlpatterns = [
    path('', views_admin.DashboardView.as_view(), name='index'),
    path('settings/', views_admin.SettingsView.as_view(), name='settings'),

    # Page Content management
    path('page-content/', include((page_content_patterns, 'page_content'), namespace='page_content')),

    # Board Members management
    path('board-members/', include((board_members_patterns, 'board_members'), namespace='board_members')),

    # Community management
    path('community/', include((community_patterns, 'community'), namespace='community')),

    # Include app-specific admin URLs with nested namespaces
    path('programs/', include(('apps.programs.urls_admin', 'programs'), namespace='programs')),
    path('batches/', include(('apps.programs.urls_admin_batches', 'batches'), namespace='batches')),
    path('coaches/', include(('apps.coaches.urls_admin', 'coaches'), namespace='coaches')),
    path('events/', include(('apps.events.urls_admin', 'events'), namespace='events')),
    path('news/', include(('apps.news.urls_admin', 'news'), namespace='news')),
    path('gallery/', include(('apps.gallery.urls_admin', 'gallery'), namespace='gallery')),
    path('blog/', include(('apps.blog.urls_admin', 'blog'), namespace='blog')),
    path('testimonials/', include(('apps.testimonials.urls_admin', 'testimonials'), namespace='testimonials')),
    path('hero-slides/', include(('apps.hero.urls_admin', 'hero'), namespace='hero')),
    path('messages/', include(('apps.contact.urls_admin', 'messages'), namespace='messages')),
    path('inquiries/', include(('apps.contact.urls_admin_inquiries', 'inquiries'), namespace='inquiries')),
    path('achievements/', include(('apps.achievements.urls_admin', 'achievements'), namespace='achievements')),
    path('accreditations/', include(('apps.accreditations.urls_admin', 'accreditations'), namespace='accreditations')),
    path('facilities/', include(('apps.facilities.urls_admin', 'facilities'), namespace='facilities')),
]
