from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Listing


@login_required
def listing(request):
    admin_listings = Listing.objects.filter(listing_type='admin')
    user_listings = Listing.objects.filter(user=request.user).exclude(listing_type='admin')
    
    context = {
        'admin_listings': admin_listings,
        'user_listings': user_listings,
    }
    return render(request, 'listings/listing.html', context)

