"""
Serializers for the Reviews application.

Handles the transformation of Review model instances into JSON and 
implements strict validation rules to prevent duplicate feedback.
"""

from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    
    Provides standardized ISO-8601 timestamps and ensures that the 
    'reviewer' field is automatically handled based on the session user.
    """
    
    # Standardizing date format for frontend consistency (ISO 8601)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", 
        read_only=True
    )
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", 
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating', 
            'description', 'created_at', 'updated_at'
        ]
        
        # User identity and timestamps are protected from manual input
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Custom validation to enforce the 'one review per business' rule.
        
        Checks if the authenticated user has already submitted a review 
        for the targeted business_user to maintain marketplace integrity.
        """
        request = self.context.get('request')
        
        # Only perform this check during the creation (POST) of a new review
        if request and request.method == 'POST':
            business_user = data.get('business_user')
            
            # Prevent duplicate feedback from the same reviewer to the same business
            if Review.objects.filter(
                reviewer=request.user, 
                business_user=business_user
            ).exists():
                raise serializers.ValidationError(
                    "You have already submitted a review for this business user."
                )
                
        return data