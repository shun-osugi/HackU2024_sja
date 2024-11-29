from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  

class CustomUser(AbstractUser):
    favorite_products = models.ManyToManyField('Product', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.username  
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='apps.products/')
    grade = models.IntegerField(choices=[(i, f'{i}年') for i in range(1, 5)])  # 学年
    faculty = models.CharField(max_length=100)  # 学部
    department = models.CharField(max_length=100, default='未設定')
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=100)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')  # カスタムユーザーを使用
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # カスタムユーザーを使用
    department_year = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # カスタムユーザーを使用
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # カスタムユーザーを使用
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.product.name}"
    