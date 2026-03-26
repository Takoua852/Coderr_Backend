"""
Custom pagination settings for the Marketplace API.

Provides a consistent structure for paginated responses, ensuring the 
frontend receives a predictable number of items per request.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

class DefaultPagination(PageNumberPagination):
    """
    Standard pagination class for offers and reviews.
    
    Attributes:
        page_size (int): Default number of items per page.
        page_size_query_param (str): Allows the client to set a custom page size via URL.
        max_page_size (int): Limits the maximum number of items a client can request.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginates the queryset while handling 'out of range' errors gracefully.
        
        If a user requests a page that does not exist (e.g., page 999), 
        instead of returning a 404 error, this returns an empty list. 
        This prevents frontend crashes and simplifies state management.
        """
        try:
            return super().paginate_queryset(queryset, request, view=view)
        except NotFound:
            # Return an empty list instead of a 404 to support smoother 
            # infinite scrolling or gallery views on the frontend.
            return []