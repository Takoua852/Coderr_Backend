"""
Signals for the Profile application.

This module automates the lifecycle of UserProfile instances, ensuring 
that every Django User has a corresponding profile created and updated 
automatically via database hooks.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a UserProfile whenever a new User is saved.
    
    This ensures that even if a user is created via the admin panel, 
    a management command, or the registration API, they always 
    possess the necessary profile metadata.
    """
    if created:
        # get_or_create is used as a safety measure to prevent 
        # IntegrityErrors in edge cases.
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to ensure the UserProfile is saved whenever 
    the User instance is updated.
    
    This maintains data consistency across the One-to-One relationship.
    """
    # hasattr check is recommended in production to avoid RelatedObjectDoesNotExist 
    # errors during specific management tasks.
    if hasattr(instance, 'profile'):
        instance.profile.save()