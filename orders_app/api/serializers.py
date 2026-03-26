"""
Serializers for the Orders application.

This module handles the serialization of service orders, ensuring that 
sensitive transaction data remains read-only after the initial creation.
"""

from rest_framework import serializers
from ..models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    
    This serializer strictly controls which fields can be modified. 
    The 'status' field is the primary editable field for business workflow 
    management, while all price and service details are locked.
    """
    price = serializers.FloatField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 
            'revisions', 'delivery_time_in_days', 'price', 
            'features', 'offer_type', 'status', 
            'created_at', 'updated_at'
        ]
        
        # Ensures that order details (the 'contract') cannot be 
        # tampered with after creation via the API.
        read_only_fields = [
            'customer_user', 'business_user', 'title', 
            'revisions', 'delivery_time_in_days', 'price', 
            'features', 'offer_type', 'created_at', 'updated_at'
        ]

    def validate_status(self, value):
        """
        Validation logic to ensure the status update matches 
        the predefined STATUS_CHOICES in the Order model.
        """
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Permitted values are: {valid_statuses}"
            )
        return value