"""
Main URL Configuration for the Freelance Marketplace API.

This module routes all incoming requests to their respective applications.
The API is structured under the 'api/' prefix to separate it from administrative 
and media routes.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BaseInfoView

urlpatterns = [
    # Standard Django Admin interface
    path('admin/', admin.site.urls),

    # Authentication endpoints (Login, Registration)
    path('api/', include('auth_app.api.urls')),

    # Core marketplace functionality: Offers, Orders, and Reviews
    path('api/', include('offers_app.api.urls')),
    path('api/', include('orders_app.api.urls')),
    path('api/', include('reviews_app.api.urls')),

    # User profile management
    path('api/', include('profile_app.api.urls')),

    # Global platform statistics for the Landing Page
    path('api/base-info/', BaseInfoView.as_view(), name='base-info')
]

# Serve media files (uploads like profile pics and offer images)
# during development when DEBUG is True.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
