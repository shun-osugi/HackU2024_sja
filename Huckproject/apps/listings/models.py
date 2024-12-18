from django.conf import settings
from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


class Listing(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,verbose_name="ID")
    grade = models.IntegerField(choices=[(i, f'{i}年') for i in range(1, 5)])  # 学年 追加
    product_name = models.CharField(max_length=128,verbose_name="商品名")
    subject = models.CharField(max_length=64,verbose_name="教科名") 
    description = models.TextField(max_length=2048,verbose_name="説明")
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000)],verbose_name="価格")
    faculty = models.CharField(max_length=64,verbose_name="学部") 
    department = models.CharField(max_length=64,verbose_name="学科") 
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/',verbose_name="画像")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')  # カスタムユーザーを使用　追加
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時追加
    
    def __str__(self):
        return self.product_name