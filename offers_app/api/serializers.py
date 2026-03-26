"""
Serializers for the Offers application.

This module handles the transformation of Offer and OfferDetail models into 
JSON format, including nested relationships, custom validation, and image handling.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for OfferDetail objects.
    Used in list views to provide only the ID and a direct link to full details.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """Generates the absolute URL for the specific offer detail endpoint."""
        request = self.context.get('request')
        path = f"/api/offerdetails/{obj.id}/"
        if request:
            return request.build_absolute_uri(path)
        return path


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for OfferDetail objects.
    Handles all fields including price, revisions, and JSON-based features.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days', 
            'price', 'features', 'offer_type'
        ]

    def to_representation(self, instance):
        """
        Ensures numeric fields are never returned as null to prevent 
        parsing errors in the frontend.
        """
        data = super().to_representation(instance)
        if data.get('revisions') is None:
            data['revisions'] = 0
        if data.get('delivery_time_in_days') is None:
            data['delivery_time_in_days'] = 0
        if data.get('price') is None:
            data['price'] = 0
        return data


class OfferSerializer(serializers.ModelSerializer):
    """
    Primary Read-Only serializer for Offer objects.
    Provides aggregated data like min_price and nested user details.
    """
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = serializers.SerializerMethodField()
    details = OfferDetailSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user_details(self, obj):
        """Flattens related user information for easier frontend access."""
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def get_image(self, obj):
        """Returns the full absolute path for the image or an empty string if null."""
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return ""


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new Offers with exactly three pricing tiers.
    """
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        """Business rule: Every offer must have exactly 3 tiers (Basic, Standard, Premium)."""
        if len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details (Basic, Standard, Premium)."
            )
        return value

    def create(self, validated_data):
        """Handles atomic creation of an Offer and its three nested OfferDetail tiers."""
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing Offers and their associated details.
    Uses offer_type as a unique key to identify which detail tier to update.
    """
    details = OfferDetailCreateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """
        Updates the main offer instance and selectively updates nested details 
        based on the offer_type (basic/standard/premium).
        """
        details_data = validated_data.pop('details', None)

        # Update base Offer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested OfferDetail tiers if provided
        if details_data is not None:
            for detail_item in details_data:
                offer_type = detail_item.get('offer_type')
                detail_instance = OfferDetail.objects.filter(
                    offer=instance,
                    offer_type=offer_type
                ).first()

                if detail_instance:
                    for attr, value in detail_item.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()

        return instance