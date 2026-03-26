from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'business_user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('description', 'reviewer__username', 'business_user__username')

    def rating_stars(self, obj):
        return "⭐" * obj.rating
    rating_stars.short_description = 'Bewertung'