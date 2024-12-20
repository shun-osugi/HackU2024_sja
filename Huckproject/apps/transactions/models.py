# models.py (transactionsアプリ)
from django.db import models
from django.conf import settings
from apps.products.models import Product

class Transaction(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller_transactions', on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer_transactions', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='pending'  # 初期値を 'pending' に設定
    )
    meeting_time = models.DateTimeField(null=True, blank=True)  # 新しいフィールド
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)