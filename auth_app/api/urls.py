"""
URL configuration for the authentication API.
Provides endpoints for user registration and login.
"""
from django.urls import path
from .views import RegistrationView, CustomLoginView

urlpatterns = [
    # POST: Create a new user account and receive an auth token
    path('registration/', RegistrationView.as_view(), name='registration'),

    # POST: Authenticate user credentials and return an auth token
    path('login/', CustomLoginView.as_view(), name='login'),
]