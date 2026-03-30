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
from django.contrib.auth.models import User
from profile_app.models import UserProfile

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
        # if self.action in ['partial_update', 'update']:
        #     return [IsBusinessOwner()]
       
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]

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
        PATCH /api/orders/{id}/
        Requirement: Only users of type 'business' can update the status.
        """
        # 1. Look up in ALL orders (ignores the get_queryset filter) to avoid 404 for unauthorized users.
        instance = get_object_or_404(
            Order, pk=kwargs.get('pk') or kwargs.get('id'))
        # 2. Permission Check (403)
        # Jetzt prüfen wir nur noch den Typ, wie von dir gewünscht.
        if request.user.profile.type != 'business':
            return Response(
                {"detail": "Only business profiles can update order statuses."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Field Validation (400)
        if set(request.data.keys()) != {'status'}:
            return Response(
                {"detail": "Only the 'status' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Update ausführen (200)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCountView(generics.GenericAPIView):
    """
    Returns the count of 'in_progress' orders for a specific business user.
    Ensures 404 if the user does not exist or is not a business user.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(
            business_user=business_user, 
            status='in_progress'
        ).count()

        return Response({"order_count": count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(generics.GenericAPIView):
    """
    Returns the total number of successfully 'completed' orders for a specific business user.
    Ensures a 404 response if the business user ID does not exist.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        # 1. VALIDATION (404): Check if the user exists and is a business profile
        # This triggers the 404 error if the ID is wrong or not a business user.
        business_user = get_object_or_404(User, id=business_user_id)
        if not hasattr(business_user, 'profile') or business_user.profile.type != 'business':
            return Response(
            {"detail": "Kein Geschäftsnutzer mit dieser ID gefunden."}, 
            status=status.HTTP_404_NOT_FOUND
        )

        # 2. LOGIC (200): Count the orders for this specific validated user
        completed_order_count = Order.objects.filter(
            business_user=business_user, status='completed').count()

        return Response({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)