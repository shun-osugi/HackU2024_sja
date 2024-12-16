# urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.google_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]