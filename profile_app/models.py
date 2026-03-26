"""
Models for the Profile application.

This module extends the default Django User model with additional metadata 
such as profile types, contact information, and business hours.
"""

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extends the base User model with domain-specific information.
    
    This model implements a One-to-One relationship with Django's built-in User,
    distinguishing between 'customer' and 'business' accounts to control 
    permissions across the platform.
    """

    ROLE_CHOICES = [
        ('customer', 'Customer'), 
        ('business', 'Business')
    ]

    # Links the profile to a unique Django User instance
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Determines the account's permissions and available features
    type = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='customer'
    )
    
    # Optional profile metadata
    file = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    location = models.CharField(max_length=255, default='', blank=True)
    tel = models.CharField(max_length=20, default='', blank=True)
    description = models.TextField(default='', blank=True)
    
    # Relevant specifically for business profiles
    working_hours = models.CharField(max_length=100, default='', blank=True)
    
    # Metadata for account age tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the username and account type for better visibility in the admin panel."""
        return f"{self.user.username} ({self.type})"