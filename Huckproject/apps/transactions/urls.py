# urls.py (transactionsアプリ)
from django.urls import path
from . import views

urlpatterns = [
    path('transaction_chat/', views.transaction_chat, name='transaction_chat'),
    path('<int:pk>/chat/', views.transaction_chat, name='transaction_chat'),  # チャットビューの追加
]