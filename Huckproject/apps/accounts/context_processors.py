from apps.products.models import UserProfile

def get_user_profile(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return {
                'user_profile': user_profile
            }
        except UserProfile.DoesNotExist:
            return {'user_profile': None}
    return {'user_profile': None} 