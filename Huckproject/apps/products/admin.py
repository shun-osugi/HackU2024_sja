from django.contrib import admin
from .models import Product, UserProfile, Comment, Favorite
from .models import CustomUser



admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Favorite)