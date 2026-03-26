"""
Views for the Reviews application.

Handles the creation and retrieval of user feedback. Includes logic to 
ensure only customers can write reviews and provides flexible filtering 
options for business profiles.
"""

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    
    Allows users to list, create, and retrieve feedback.
    Includes built-in support for ordering by date or rating score.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    # Enables API consumers to sort results (e.g., ?ordering=-rating)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']

    def get_queryset(self):
        """
        Dynamically filters reviews based on query parameters.
        Allows fetching all reviews for a specific business or by a specific author.
        """
        queryset = Review.objects.all()
        
        # Extract filter parameters from the URL
        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')
        
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
            
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Custom creation logic for reviews.
        
        Validates that the author has a 'customer' profile type and 
        automatically assigns the logged-in user as the reviewer.
        """
        # Business Rule: Only customers can rate service providers
        if request.user.profile.type != 'customer':
            return Response(
                {"detail": "Only customer profiles are allowed to create reviews."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the review while injecting the authenticated user as the reviewer
        serializer.save(reviewer=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)