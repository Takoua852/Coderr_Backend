from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_user', 'business_user', 'title', 'status', 'price', 'delivery_time_in_days')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'customer_user__username', 'business_user__username')
    list_editable = ('status',) 