from django.shortcuts import render
from apps.listings.models import Listing


def index(request):
    return render(request, 'mypage.html')

def buy_record(request):#購入履歴
    return render(request, 'buy_record.html')

def member_info(request):#会員情報
    return render(request, 'member_info.html')

def inquiry(request):#お問い合わせ
    return render(request, 'inquiry.html')

def transaction(request):
    return render(request, 'transaction.html')

def listing_record(request):#出品履歴
    # Listing モデルの全データを取得
    listings = Listing.objects.all()
    # テンプレートにデータを渡す
    return render(request, 'listing_record.html', {'listings': listings})
