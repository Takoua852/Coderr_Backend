from django.contrib import admin
from django.utils.html import format_html
from .models import Offer, OfferDetail

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 3  # Zeigt standardmäßig 3 leere Reihen für Details
    max_num = 3

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'min_price_display', 'image_tag', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'description')
    inlines = [OfferDetailInline]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Vorschau'

    def min_price_display(self, obj):
        # Zeigt den kleinsten Preis der Details in der Liste an
        details = obj.details.all()
        if details:
            return f"{min(d.price for d in details)} €"
        return "-"
    min_price_display.short_description = 'Ab Preis'