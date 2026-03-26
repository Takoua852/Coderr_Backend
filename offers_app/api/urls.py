"""
URL configuration for the Offers application.

This module defines the routes for accessing and managing service offers, 
including listing, creating, and retrieving specific offer tiers.
"""

from django.urls import path
from .views import OfferListCreateView, OfferDetailView, OfferDetailRetrieveView

urlpatterns = [
    # GET: List all offers (with filtering/sorting)
    # POST: Create a new offer (Business users only)
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    
    # GET: Retrieve a specific offer
    # PUT/PATCH: Update an offer (Owner only)
    # DELETE: Remove an offer (Owner only)
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    
    # GET: Retrieve full details of a specific pricing tier (Basic, Standard, or Premium)
    path('offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offerdetail-detail')
]