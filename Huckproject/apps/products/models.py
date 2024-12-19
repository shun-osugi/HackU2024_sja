from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings  
from django.contrib.auth import get_user_model


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
    description = models.TextField(max_length=2048, verbose_name="説明", default='説明なし')  # 商品説明を追加
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')  # カスタムユーザーを使用
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchased_products')  # 購入者を追加
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # accountsアプリから統合するフィールド
    account_name = models.CharField(max_length=100, default="Default Name")
    email = models.EmailField(unique=True, default="default@ccmailg.meijo-u.ac.jp") #メールアドレス
    faculty = models.CharField(max_length=255, default='未設定')  # 学部
    department = models.CharField(max_length=100)  # 学科
    password = models.CharField(max_length=128, null=True, blank=True)# パスワード
    grade = models.CharField(max_length=50, default='未設定')     # 学年
    product_name = models.CharField(max_length=100, default='未設定')  # 商品名
    availability = models.JSONField(default=list)  # 空き時間を保存するフィールド

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
