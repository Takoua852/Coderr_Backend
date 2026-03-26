"""
Views for the Orders application.

Handles the lifecycle of service orders, including creation from offer tiers,
status updates by business owners, and statistical counters.
"""

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomerUser, IsBusinessOwner, IsAdminUser
from offers_app.models import OfferDetail

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing service orders.
    
    Provides standard CRUD actions with custom logic for creation and partial updates.
    Ensures that users only see orders where they are either the buyer or the seller.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        Dynamically assigns permissions based on the action:
        - create: Restricted to customer profiles.
        - update/partial_update: Restricted to the business owner of the order.
        - destroy: Restricted to administrators.
        - list/retrieve: Accessible to any authenticated user involved in the order.
        """
        if self.action == 'create':
            return [IsCustomerUser()]
        if self.action in ['partial_update', 'update']:
            return [IsBusinessOwner()]
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Filters the orders so users only access their own transactions.
        Uses a complex Q-filter to include both customer and business roles.
        """
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def create(self, request):
        """
        Creates a new Order instance by copying data from a specific OfferDetail.
        This acts as a 'checkout' process, creating a snapshot of the price and features.
        """
        offer_detail_id = request.data.get('offer_detail_id')
        offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)
        
        # Mapping offer detail attributes to a permanent order record
        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """
        Allows business owners to update the status of an order.
        Strictly limits updates to the 'status' field to prevent tampering with price or title.
        """
        if 'status' in request.data and len(request.data) == 1:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            {"detail": "Only the 'status' field is allowed to be updated."}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderCountView(generics.RetrieveAPIView):
    """
    Returns the number of currently active ('in_progress') orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, business_user_id):
        count = Order.objects.filter(business_user_id=business_user_id, status='in_progress').count()
        return Response({"order_count": count})

class CompletedOrderCountView(generics.RetrieveAPIView):
    """
    Returns the total number of successfully 'completed' orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, business_user_id):
        count = Order.objects.filter(business_user_id=business_user_id, status='completed').count()
        return Response({"completed_order_count": count})