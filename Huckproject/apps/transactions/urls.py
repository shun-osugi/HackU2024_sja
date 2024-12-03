# urls.py (transactionsアプリ)
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/chat/', views.transaction_chat, name='transaction_chat'),  # チャットビューの追加
]