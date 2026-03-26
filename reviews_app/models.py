"""
Models for the Reviews application.

This module handles the feedback system, allowing customers to rate 
business users. It includes strict validation for ratings and 
prevents duplicate reviews.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Represents a rating and feedback given by a customer to a business provider.
    
    Includes built-in Django validators to ensure ratings stay within 
    the 1-5 star range and database-level constraints to ensure 
    one review per customer-business pair.
    """

    # The provider being reviewed
    business_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews_received'
    )
    
    # The customer writing the review
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews_written'
    )
    
    # Numerical rating with strict range validation (1 to 5 stars)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Detailed feedback text
    description = models.TextField()
    
    # Timestamps for tracking review history
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Database constraints and metadata.
        Ensures a user can only review a specific business once.
        """
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        """Returns a readable summary of the review, including the rating score."""
        return f"Review from {self.reviewer} for {self.business_user} ({self.rating}/5)"