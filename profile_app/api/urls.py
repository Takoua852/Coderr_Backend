"""
URL configuration for the Profile application.

Includes routes for managing individual user profiles and listing 
profiles filtered by account type (Business or Customer).
"""

from django.urls import path
from .views import (
    UserProfileDetailView, 
    BusinessProfileListView, 
    CustomerProfileListView
)

urlpatterns = [
    # GET: Retrieve a specific user profile by User ID
    # PATCH/PUT: Update the profile (Owner only)
    path('profile/<int:user_id>/', UserProfileDetailView.as_view(), name='profile-detail'),

    # GET: List all profiles with the 'business' type
    path('profiles/business/', BusinessProfileListView.as_view(), name='business-profiles'),

    # GET: List all profiles with the 'customer' type
    path('profiles/customer/', BusinessProfileListView.as_view(), name='customer-profiles'),
]