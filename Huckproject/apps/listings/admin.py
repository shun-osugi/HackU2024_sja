from django.contrib import admin
from .models import Listing
from django.contrib import admin
from .models import AdminListing

admin.site.register(AdminListing)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing_type', 'content', 'created_at', 'is_read')
    list_filter = ('listing_type', 'is_read')
    search_fields = ('content',)