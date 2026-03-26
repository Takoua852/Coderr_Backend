"""
Custom permissions for the marketplace.
Defines access levels for business operations and object ownership.
"""

from rest_framework import permissions

class IsBusinessProfileOrReadOnly(permissions.BasePermission):
    """
    Global permission check:
    Allows anyone to read (GET), but only users with a 'business' profile 
    type can perform write operations (POST, PUT, DELETE).
    """

    def has_permission(self, request, view):
        """
        Check if the user has the required profile type for the requested action.
        """
        # SAFE_METHODS like GET, HEAD, or OPTIONS are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # For writing, user must be logged in and have a business profile
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.type == 'business'
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission check:
    Ensures that only the creator/owner of an object can modify or delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the authenticated user is the actual owner of the data instance.
        """
        # Read-only access is granted to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write access is only granted if the object belongs to the current user
        return obj.user == request.user