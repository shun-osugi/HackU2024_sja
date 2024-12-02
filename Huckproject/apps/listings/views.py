from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Listings


@login_required
def listings(request):
    admin_listings = Listings.objects.filter(listings_type='admin')
    user_listings = Listings.objects.filter(user=request.user).exclude(listings_type='admin')
    
    context = {
        'admin_listings': admin_listings,
        'user_listings': user_listings,
    }
    return render(request, 'listings/listings.html', context)

