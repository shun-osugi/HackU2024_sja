from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings  
from django.utils import timezone

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
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # accountsアプリから統合するフィールド
    account_name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(unique=True, default="default@ccmailg.meijo-u.ac.jp") #メールアドレス
    department = models.CharField(max_length=100)  # 学部・学科
    password = models.CharField(max_length=128, null=True, blank=True) 
    grade = models.IntegerField(null=True, blank=True)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        """
        モデル保存時にパスワードをハッシュ化します。
        """
        if self.password and not self.password.startswith('pbkdf2_'):  # 既にハッシュ化されている場合はスキップ
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # productsアプリの既存のフィールド
    # （既存のフィールドがあればそのまま残す）

    def __str__(self):
        return self.account_name

    class Meta:
        app_label = 'products'


class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"
    
# お気に入り機能をコメントアウト
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # カスタムユーザーを使用
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.product.name}"
