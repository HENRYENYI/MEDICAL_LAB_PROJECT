"""
URL configuration for medical_lab project.
"""
from django.contrib import admin
from django.urls import path, include

# For serving static & media files in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main Site URLs
    path('', include('core.urls')),
    
    # App URLs
    path('tests/', include('tests.urls')),
    path('booking/', include('bookings.urls')),
    path('consultation/', include('consultation.urls')), 
    path('accounts/', include('users.urls')),
    
    # Django Admin URL
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
