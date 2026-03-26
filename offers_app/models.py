from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    """
    Represents a service offered by a business user.
    Acts as the parent container for different pricing tiers (OfferDetails).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """
    Represents a specific pricing tier for an Offer (Basic, Standard, or Premium).
    Stores specific metadata like delivery time, price, and custom features.
    """
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'), 
        ('standard', 'Standard'), 
        ('premium', 'Premium')
    ]
    
    # Links the detail to a specific parent offer
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Stores a list of strings representing the features included in this tier
    features = models.JSONField() 
    
    offer_type = models.CharField(
        max_length=10, 
        choices=OFFER_TYPE_CHOICES
    )

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"