from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    admin_notifications = Notification.objects.filter(notification_type='admin')
    user_notifications = Notification.objects.filter(user=request.user).exclude(notification_type='admin')
    
    context = {
        'admin_notifications': admin_notifications,
        'user_notifications': user_notifications,
    }
    return render(request, 'notifications/notification_list.html', context)

