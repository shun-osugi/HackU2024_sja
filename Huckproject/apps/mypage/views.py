from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.products.models import Product, Favorite, UserProfile


def index(request):
    return render(request, 'mypage.html')

def favorite(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'favorite.html', {'favorites': favorites})

@login_required
def buy_record(request):#購入履歴
    # ログインしているユーザーの購入履歴を取得
    purchases = Product.objects.filter(buyer=request.user).order_by('-updated_at')
    return render(request, 'buy_record.html', {'purchases': purchases})

def member_info(request):#会員情報
    user_profile = get_object_or_404(UserProfile, user=request.user)  # 現在のユーザーのプロファイルを取得
    context = {
        'availability': user_profile.availability,  # availabilityをテンプレートに渡す
    }
    return render(request, 'mypage/member_info.html', context)

def inquiry(request):#お問い合わせ
    return render(request, 'inquiry.html')


def transaction(request):
    return render(request, 'transaction.html')

def inquiry_thanks(request):#お問い合わせありがとう
    return render(request, 'thanks.html')

@login_required
def member_info(request):
    # ログインしているユーザーのUserProfileを取得
    user_profile = get_object_or_404(UserProfile, user=request.user)
    print("空き時間デバッグ:", user_profile.availability)  # データ構造を確認
    context = {
        'availability': user_profile.availability,
    }
    return render(request, 'member_info.html', context)

@login_required
def listing_record(request):#出品履歴
    # ログインしているユーザの出品履歴を取得
    listings = Product.objects.filter(seller=request.user).order_by('-created_at')
    # テンプレートにデータを渡す
    return render(request, 'listing_record.html', {'listings': listings})
