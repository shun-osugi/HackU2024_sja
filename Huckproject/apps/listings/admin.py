from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'subject', 'price', 'faculty', 'department')
    search_fields = ('product_name', 'subject', 'faculty', 'department')
