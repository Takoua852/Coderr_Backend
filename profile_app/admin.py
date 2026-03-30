from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'type', 'location', 'avatar_tag')
    list_filter = ('type',)
    search_fields = ('user__username', 'location', 'tel')

    def avatar_tag(self, obj):
        if obj.file:
            return format_html('<img src="{}" style="width: 40px; height:40px; border-radius: 50%;" />', obj.file.url)
        return "Kein Bild"
    avatar_tag.short_description = 'Profilbild'