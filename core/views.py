from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from rest_framework.permissions import AllowAny

from reviews_app.models import Review
from profile_app.models import UserProfile 
from offers_app.models import Offer 

class BaseInfoView(APIView):
    """
    API view to provide general marketplace statistics.
    Returns aggregated data for the landing page hero section, 
    including review counts, average ratings, and totals for profiles and offers.
    """
    permission_classes = [AllowAny] 

    def get(self, request):
        """
        Retrieves and calculates total counts and averages across the platform.
        """
        try:
            # Aggregate platform-wide review statistics
            review_count = Review.objects.count()
            avg_rating_query = Review.objects.aggregate(Avg('rating'))['rating__avg']
            average_rating = round(avg_rating_query, 1) if avg_rating_query else 0.0

            # Count profiles specifically registered as business accounts
            business_profile_count = UserProfile.objects.filter(type='business').count()

            # Count total number of service offers available
            offer_count = Offer.objects.count()

            return Response({
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count
            }, status=status.HTTP_200_OK)

        except Exception:
            # Fallback error message in English for professional consistency
            return Response(
                {"detail": "Internal server error during statistics calculation."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )