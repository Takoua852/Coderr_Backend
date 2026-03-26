from .utils import validate_int_param
from rest_framework import generics, filters
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import OfferSerializer, OfferCreateSerializer, OfferUpdateSerializer, OfferDetailCreateSerializer
from ..models import Offer, OfferDetail
from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class OfferListCreateView(generics.ListCreateAPIView):
    """
    View for listing all offers and creating new ones.
    Includes advanced filtering by price, delivery time, and creator.
    """
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_serializer_class(self):
        """
        Returns OfferCreateSerializer for POST requests 
        and the standard OfferSerializer for GET requests.
        """
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer

    def get_queryset(self):
        """
        Retrieves offers with annotated minimum price and delivery time 
        calculated from the related OfferDetail tiers.
        """
        queryset = Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        ).order_by('-updated_at')

        # Custom filtering based on query parameters
        creator_id = validate_int_param(self.request, "creator_id")
        min_price = validate_int_param(self.request, "min_price")
        max_delivery_time = validate_int_param(
            self.request, "max_delivery_time")

        if creator_id:
            queryset = queryset.filter(user_id=creator_id)
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)
        if max_delivery_time:
            queryset = queryset.filter(
                min_delivery_time__lte=max_delivery_time)

        return queryset

    def perform_create(self, serializer):
        """
        Validates if the user is a business profile before creating an offer.
        Assigns the current authenticated user as the offer creator.
        """
        if self.request.user.profile.type != 'business':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Nur Business-Profile dürfen Angebote erstellen.")

        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific offer.
    Implements ownership-based permission for modification and deletion.
    """
    queryset = Offer.objects.annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    ).all()

    def get_serializer_class(self):
        """
        Returns OfferUpdateSerializer for partial or full updates.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return OfferUpdateSerializer
        return OfferSerializer

    def get_permissions(self):
        """
        Restricts update and delete actions to the owner of the offer.
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """
    Dedicated view to retrieve full details of a single pricing tier (OfferDetail).
    Used when the frontend needs deep data for a specific package (Basic/Standard/Premium).
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailCreateSerializer
    permission_classes = [IsAuthenticated]
