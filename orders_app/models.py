"""
Models for the Orders application.

This module defines the Order entity, which represents a contract between 
a customer and a business user based on a specific service offer.
"""

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    """
    Represents a finalized purchase of a service.
    Stores a snapshot of the offer details (price, revisions, etc.) at the 
    time of purchase to ensure record integrity even if the original offer changes.
    """

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Relationships to the User model, distinguishing between buyer and seller
    customer_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='customer_orders'
    )
    business_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='business_orders'
    )

    # Snapshot of the service details
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # List of features included in this specific order
    features = models.JSONField()
    
    # Tier type (e.g., basic, standard, premium)
    offer_type = models.CharField(max_length=50)

    # Order lifecycle management
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='in_progress'
    )
    
    # Timestamps for auditing and history
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a string representation of the order with its ID and title."""
        return f"Order #{self.id} - {self.title}"