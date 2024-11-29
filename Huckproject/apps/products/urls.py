from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('product/<int:product_id>/add_comment/', views.add_comment, name='add_comment'),  # この行を追加
    path('transaction/<int:product_id>/', views.transaction_page, name='transaction_page'),
]