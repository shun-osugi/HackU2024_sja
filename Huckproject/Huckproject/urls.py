"""
URL configuration for Huckproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
import os

from apps.home import views as home_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='root'),  # ルートURLを/accounts/login/にリダイレクト
    path('accounts/', include('apps.accounts.urls')),
    path('home/', include('apps.home.urls')),
    path('listings/', include('apps.listings.urls')),
    path('mypage/', include('apps.mypage.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('transactions/', include('apps.transactions.urls')),
    path('products/', include('apps.products.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)