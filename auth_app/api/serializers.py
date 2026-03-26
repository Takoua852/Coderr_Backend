from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation along with their associated profile type.
    """
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Custom validation to check password matching and email uniqueness.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwörter stimmen nicht überein."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Diese E-Mail wird bereits verwendet."})
        return data

    def create(self, validated_data):
        """
        Creates a new User and updates the automatically created profile with the selected type.
        Uses an atomic transaction to ensure both User and Profile are handled correctly.
        """
        with transaction.atomic():
            user_type = validated_data.pop('type')
            validated_data.pop('repeated_password')
            
            user = User.objects.create_user(**validated_data)
            user.profile.type = user_type
            user.profile.save()
            
            return user