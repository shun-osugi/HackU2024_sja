from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.index, name='mypage'),
    path('buy_record/', views.buy_record, name='buy_record'),#購入履歴
    path('member_info/', views.member_info, name='member_info'),#会員情報
    path('inquiry/', views.inquiry, name='inquiry'),#お問い合わせ
    path('listing_record/', views.listing_record, name='listing_record'),#出品履歴
]