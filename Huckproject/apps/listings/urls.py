from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'listings'

urlpatterns = [
    path('create/', views.create_listing, name='listing'),
    path('edit/<int:product_id>/', views.edit_listing, name='edit_listing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)