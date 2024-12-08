# Generated by Django 4.2.16 on 2024-12-07 08:50

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=128, verbose_name='商品名')),
                ('subject', models.CharField(max_length=64, verbose_name='教科名')),
                ('description', models.TextField(max_length=2048, verbose_name='説明')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='価格')),
                ('faculty', models.CharField(max_length=64, verbose_name='学部')),
                ('department', models.CharField(max_length=64, verbose_name='学科')),
                ('image', models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='画像')),
            ],
        ),
    ]