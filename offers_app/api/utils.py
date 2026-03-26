"""
Utility functions for input validation and parameter cleaning.
Ensures that query parameters from the frontend are safely parsed before 
being used in database queries.
"""

from rest_framework.exceptions import ValidationError

def validate_int_param(request, param_name):
    """
    Safely extracts and parses an integer from query parameters.
    Handles empty values, whitespace, and common typographical 
    noise (like curly or double quotes).
    
    Returns:
        int: The cleaned integer value.
        None: If the parameter is missing or effectively empty.
    
    Raises:
        ValidationError: If the provided value cannot be converted to an integer.
    """
    value = request.query_params.get(param_name)
    
    # Check if the parameter is missing, empty, or just contains quotes
    if value is None or value == "" or value == "“" or value == '""':
        return None

    try:
        # Sanitize input: strip whitespace and remove various quote characters
        # (Useful for mobile/OSX smart-quotes or accidental frontend stringification)
        clean_value = str(value).replace('“', '').replace('”', '').replace('"', '').strip()
        
        if not clean_value:
            return None
            
        return int(clean_value)
        
    except (ValueError, TypeError):
        # Raise a 400 Bad Request instead of allowing a 500 Internal Server Error
        raise ValidationError({
            param_name: f"The value '{value}' is not a valid integer."
        })