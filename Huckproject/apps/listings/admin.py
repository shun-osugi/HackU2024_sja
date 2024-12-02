from django.contrib import admin
from .models import Listings
from django.contrib import admin
from .models import AdminListings

admin.site.register(AdminListings)

@admin.register(Listings)
class listingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listings_type', 'content', 'created_at', 'is_read')
    list_filter = ('listings_type', 'is_read')
    search_fields = ('content',)