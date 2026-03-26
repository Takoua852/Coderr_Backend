"""
URL configuration for the Orders application.

This module sets up the routing for order management using a DefaultRouter 
for standard CRUD actions and explicit paths for statistical endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderCountView, CompletedOrderCountView

# Standard RESTful routing for the OrderViewSet (list, create, retrieve, update)
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # Router-generated URLs: /api/orders/
    path('', include(router.urls)),
    
    # GET: Retrieve the number of active ('in_progress') orders for a specific business
    path(
        'order-count/<int:business_user_id>/', 
        OrderCountView.as_view(), 
        name='order-count'
    ),
    
    # GET: Retrieve the number of 'completed' orders for a specific business
    path(
        'completed-order-count/<int:business_user_id>/', 
        CompletedOrderCountView.as_view(), 
        name='completed-order-count'
    ),
]