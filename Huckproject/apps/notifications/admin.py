from django.contrib import admin
from .models import Notification
from django.contrib import admin
from .models import AdminNotification

admin.site.register(AdminNotification)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'content', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('content',)