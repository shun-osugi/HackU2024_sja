# Generated by Django 5.1.3 on 2024-12-20 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_merge_20241220_1353"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="availability",
            field=models.JSONField(default=list),
        ),
    ]
