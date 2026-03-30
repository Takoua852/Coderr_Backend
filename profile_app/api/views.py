"""
Views for the Profile application.

Provides endpoints for retrieving and updating user profiles, 
as well as listing profiles filtered by their account type (Business or Customer).
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from profile_app.models import UserProfile
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint for retrieving and updating a specific user profile.
    
    Uses 'user_id' as the lookup field to allow direct access via the 
    User's primary key. Updates are forced to be partial (PATCH-style) 
    to simplify frontend integration.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'user_id'
    pagination_class = None

    def update(self, request, *args, **kwargs):
        """
        Overrides the default update method to enforce partial updates.
        This allows clients to update individual fields without 
        submitting the entire profile object.
        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class BusinessProfileListView(generics.ListAPIView):
    """
    Provides a list of all profiles registered as 'business' accounts.
    Used for the provider directory or search results.
    """
    serializer_class = BusinessProfileSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns only profiles with the 'business' type."""
        return UserProfile.objects.filter(type='business')
    

class CustomerProfileListView(generics.ListAPIView):
    """
    Provides a list of all profiles registered as 'customer' accounts.
    Typically utilized for administrative overviews.
    """
    serializer_class = CustomerProfileSerializer
    pagination_class = None 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Returns only profiles with the 'customer' type."""
        return UserProfile.objects.filter(type='customer')