"""
Custom permissions for the Orders application.

This module provides granular access control to distinguish between 
customer actions (buying), business owner actions (managing orders), 
and administrative overrides.
"""

from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """
    Global permission: 
    Allows access only to authenticated users with a 'customer' profile type.
    Typically used for creating new orders.
    """

    def has_permission(self, request, view):
        """
        Verifies that the user is authenticated and is registered as a customer.
        """
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'customer'
        )

class IsBusinessOwner(permissions.BasePermission):
    """
    Object-level permission: 
    Allows access only if the authenticated user is the designated 
    'business_user' for a specific order and holds a 'business' profile.
    """
   
    def has_object_permission(self, request, view, obj):
        """
        Checks if the user is the owner of the service being sold in the order.
        """
        return bool(
            request.user and 
            request.user.is_authenticated and 
            obj.business_user == request.user and 
            request.user.profile.type == 'business'
        )

class IsAdminUser(permissions.BasePermission):
    """
    Administrative permission:
    Grants access only to users with the 'is_staff' flag enabled in Django.
    Used for sensitive operations like deleting orders.
    """
    
    def has_permission(self, request, view):
        """
        Strict check for Django staff status.
        """
        return bool(request.user and request.user.is_staff)