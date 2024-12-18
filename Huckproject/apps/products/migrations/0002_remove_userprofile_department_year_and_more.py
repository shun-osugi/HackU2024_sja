# Generated by Django 5.1.3 on 2024-12-14 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="department_year",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="rating",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="account_name",
            field=models.CharField(default="Default Name", max_length=100),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="department",
            field=models.CharField(default="Default Name", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(
                default="default@ccmailg.meijo-u.ac.jp", max_length=254, unique=True
            ),
            preserve_default=False,
        ),
    ]