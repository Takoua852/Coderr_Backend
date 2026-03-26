"""
URL configuration for the Reviews application.

This module utilizes a DefaultRouter to automatically generate 
RESTful endpoints for the ReviewViewSet, including listing, 
retrieving, and creating feedback.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

# Initialize the router and register the ReviewViewSet.
# This automatically handles:
# GET /api/reviews/          -> list
# POST /api/reviews/         -> create
# GET /api/reviews/{id}/     -> retrieve
# DELETE /api/reviews/{id}/  -> destroy (if implemented)
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    # Include all router-generated URLs
    path('', include(router.urls)),
]