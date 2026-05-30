"""
URL configuration for phishing_platform project.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls')),  # Public guest website
    path('accounts/', include('accounts.urls')),
    path('learn/', include('education.urls')),
    path('simulations/', include('simulations.urls')),
    path('assessments/', include('assessments.urls')),
    path('analytics/', include('analytics.urls')),
    path('quiz/', include('quiz.urls')),
    path('manage/', include('admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
