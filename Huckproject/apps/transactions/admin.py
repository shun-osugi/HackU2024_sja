# admin.py (transactionsアプリ)
from django.contrib import admin
from .models import Transaction, Message

admin.site.register(Transaction)
admin.site.register(Message)