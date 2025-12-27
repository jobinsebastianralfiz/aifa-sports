"""
URL configuration for AIFA Sports Academy.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('health/', health_check, name='health_check'),
    # Django Admin (keep for development)
    path('django-admin/', admin.site.urls),

    # Authentication
    path('', include('apps.accounts.urls')),

    # Custom Admin Dashboard
    path('dashboard/', include('apps.core.urls_admin', namespace='admin_dashboard')),

    # Frontend (Public Website)
    path('', include('apps.core.urls_frontend', namespace='frontend')),
    path('programs/', include('apps.programs.urls', namespace='programs')),
    path('coaches/', include('apps.coaches.urls', namespace='coaches')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('news/', include('apps.news.urls', namespace='news')),
    path('gallery/', include('apps.gallery.urls', namespace='gallery')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('achievements/', include('apps.achievements.urls', namespace='achievements')),
    path('accreditations/', include('apps.accreditations.urls', namespace='accreditations')),
    path('facilities/', include('apps.facilities.urls', namespace='facilities')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    # Serve frontend assets at root level (for HTML templates that use ../css/, ../assets/)
    FRONTEND_DIR = settings.BASE_DIR / 'frontend'
    urlpatterns += static('/css/', document_root=FRONTEND_DIR / 'css')
    urlpatterns += static('/js/', document_root=FRONTEND_DIR / 'js')
    urlpatterns += static('/assets/', document_root=FRONTEND_DIR / 'assets')

    # Serve admin assets
    ADMIN_DIR = settings.BASE_DIR / 'admin'
    urlpatterns += static('/admin-css/', document_root=ADMIN_DIR / 'css')
    urlpatterns += static('/admin-js/', document_root=ADMIN_DIR / 'js')
