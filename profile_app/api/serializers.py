"""
Serializers for the Profile application.

This module provides a unified interface for the UserProfile model, 
flattening related data from the Django User model to simplify 
frontend integration.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    A comprehensive serializer for user profiles.

    It bridges the UserProfile and the standard Django User models, 
    allowing 'first_name', 'last_name', and 'email' to be updated 
    directly through the profile endpoint.
    """

    # Flattening fields from the related User model using 'source'
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(
        source='user.first_name',
        allow_blank=True,
        default=''
    )
    last_name = serializers.CharField(
        source='user.last_name',
        allow_blank=True,
        default=''
    )

    # Sanitizing optional fields to ensure consistent string types
    # instead of null values for the frontend.
    location = serializers.CharField(allow_blank=True, default='')
    tel = serializers.CharField(allow_blank=True, default='')
    description = serializers.CharField(allow_blank=True, default='')
    working_hours = serializers.CharField(allow_blank=True, default='')

    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ",
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'created_at'
        ]
        # Prevents modification of core identity and account type through this endpoint
        read_only_fields = ['user', 'type', 'created_at']

    def update(self, instance, validated_data):
        """
        Custom update logic to handle data across two models.
        Extracts nested user data and updates the User model before 
        proceeding with the standard UserProfile update.
        """
        # Pop the nested 'user' data (containing first_name, last_name, email)
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update specific fields on the core Django User instance
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        # Update the UserProfile instance with the remaining data
        return super().update(instance, validated_data)


class CustomerProfileSerializer(UserProfileSerializer):
    """Specialized serializer for Customer listings."""
    # Mapping 'created_at' to 'uploaded_at' as per your example
    uploaded_at = serializers.DateTimeField(
        source='created_at', read_only=True)

    class Meta(UserProfileSerializer.Meta):
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'uploaded_at', 'type'
        ]


class BusinessProfileSerializer(UserProfileSerializer):
    """Specialized serializer for Business listings."""
    class Meta(UserProfileSerializer.Meta):
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type'
        ]
