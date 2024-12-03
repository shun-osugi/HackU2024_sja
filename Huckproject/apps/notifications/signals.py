# your_app/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from .models import Comment, Product, Transaction, Favorite

@receiver(post_save, sender=Comment)
def notify_product_owner_of_comment(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product_url = reverse('product_detail', args=[product.id])
        full_url = f'http://example.com{product_url}'  # 実際のドメインに置き換えてください
        send_mail(
            '新しいコメントがあります',
            f'あなたの商品 "{product.name}" に新しいコメントがありました。\n商品ページ: {full_url}',
            'noreply@example.com',
            [product.seller.email],
            fail_silently=False,
        )

@receiver(pre_save, sender=Product)
def notify_price_drop(sender, instance, **kwargs):
    if instance.id:  # 既存の商品の場合
        old_instance = Product.objects.get(id=instance.id)
        if instance.price < old_instance.price:
            product_url = reverse('product_detail', args=[instance.id])
            full_url = f'http://example.com{product_url}'  # 実際のドメインに置き換えてください
            for favorite in Favorite.objects.filter(product=instance):
                send_mail(
                    '商品の値下げがありました',
                    f'お気に入りの商品 "{instance.name}" が値下げされました。\n新価格: {instance.price}円\n商品ページ: {full_url}',
                    'noreply@example.com',
                    [favorite.user.email],
                    fail_silently=False,
                )

@receiver(post_save, sender=Transaction)
def notify_transaction_complete(sender, instance, **kwargs):
    if instance.status == 'completed':
        transaction_url = reverse('transaction_detail', args=[instance.id])  # この URL 名は実際のプロジェクトに合わせて変更してください
        full_url = f'http://example.com{transaction_url}'  # 実際のドメインに置き換えてください
        send_mail(
            '取引完了の確認とレビューのお願い',
            f'取引が完了しました。取引確認ボタンを押してください。\nまた、取引相手へのレビューをお願いします。\n取引ページ: {full_url}',
            'noreply@example.com',
            [instance.buyer.email, instance.seller.email],
            fail_silently=False,
        )

# 取引確認ボタンの通知（取引ステータスが変更されたときに送信）
@receiver(pre_save, sender=Transaction)
def notify_transaction_confirmation(sender, instance, **kwargs):
    if instance.id:
        old_instance = Transaction.objects.get(id=instance.id)
        if old_instance.status != 'completed' and instance.status == 'completed':
            transaction_url = reverse('transaction_detail', args=[instance.id])  # この URL 名は実際のプロジェクトに合わせて変更してください
            full_url = f'http://example.com{transaction_url}'  # 実際のドメインに置き換えてください
            send_mail(
                '取引確認のお願い',
                f'取引が完了しました。取引確認ボタンを押してください。\n取引ページ: {full_url}',
                'noreply@example.com',
                [instance.buyer.email, instance.seller.email],
                fail_silently=False,
            )