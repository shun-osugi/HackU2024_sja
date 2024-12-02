from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import listings


@login_required
def listings(request):
    admin_listings = listings.objects.filter(listings_type='admin')
    user_listings = listings.objects.filter(user=request.user).exclude(listings_type='admin')
    
    context = {
        'admin_listings': admin_listings,
        'user_listings': user_listings,
    }
    return render(request, 'listings/listings.html', context)

