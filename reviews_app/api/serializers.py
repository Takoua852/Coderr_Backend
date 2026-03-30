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
    rating = serializers.IntegerField(min_value=1, max_value=5)
    description = serializers.CharField()
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
        request = self.context.get('request')
        # .get() gibt None zurück, wenn das Feld im PATCH fehlt
        business_user = data.get('business_user')

        # PRÜFUNG NUR BEI POST ODER WENN DAS FELD IM PATCH ENTHALTEN IST
        if business_user:
            # 1. Sicherstellen, dass der Empfänger ein Business-Profil hat
            if not hasattr(business_user, 'profile') or business_user.profile.type != 'business':
                raise serializers.ValidationError(
                    {"business_user": "Reviews can only be given to users with a business profile."}
                )

            # 2. Check: Man darf sich nicht selbst bewerten
            if request and business_user == request.user:
                raise serializers.ValidationError(
                    "You cannot review yourself.")

        # 3. Double-Review Check (Nur bei neuem Erstellen relevant)
        if request and request.method == 'POST' and business_user:
            if Review.objects.filter(reviewer=request.user, business_user=business_user).exists():
                raise serializers.ValidationError(
                    "You have already submitted a review for this business user."
                )

        return data
