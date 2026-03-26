"""
Custom permissions for the Profile application.

Ensures that while profiles are publicly viewable, only the 
rightful owner has the authority to modify their personal information.
"""

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a 'user' attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request is a safe read-only operation or 
        if the user is the owner of the specific object.
        """
        # Read permissions are allowed to any request,
        # so we always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user