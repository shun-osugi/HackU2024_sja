from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

class Listings(models.Model):
    LISTINGS_TYPES = (
        ('admin', '運営からのお知らせ'),
        ('comment', 'コメント通知'),
        ('transaction', '取引通知'),
        ('review', 'レビュー依頼'),
        ('price_drop', '値下げ通知'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    listings_type = models.CharField(max_length=20, choices=LISTINGS_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_listings_type_display()} - {self.content[:50]}"
    
    
User = get_user_model()

class AdminListings(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title