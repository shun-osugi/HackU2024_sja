from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.products.models import Product, Favorite, UserProfile
import logging  # ログ出力用
from django.db.models import Q
from apps.transactions.models import Transaction, Message
from .forms import MessageForm, MeetingTimeForm
from django.contrib.auth import get_user_model

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

logger = logging.getLogger(__name__)

@login_required
def transaction_list(request, user_id):
    # 対象ユーザーを取得
    User = get_user_model()
    target_user = get_object_or_404(User, id=user_id)

    # 対象ユーザーが関与しているステータスが「pending」の取引を取得
    transactions = Transaction.objects.filter(
        Q(seller=target_user) | Q(buyer=target_user),
        status='pending'
    )

    return render(request, 'mypage/transaction_list.html', {'transactions': transactions, 'target_user': target_user})

@login_required
def transaction(request):
    # ログインしているユーザーが関与している取引を取得
    transactions = Transaction.objects.filter(
        Q(seller=request.user) | Q(buyer=request.user)
    )
    return render(request, 'mypage/transaction.html', {'transactions': transactions})

@login_required
def transaction_chat(request, pk):
    # 取引を取得
    transaction = get_object_or_404(Transaction, pk=pk)

    # メッセージフォームを処理
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.transaction = transaction
            message.sender = request.user
            message.save()
            return redirect('transaction_chat', pk=pk)
    else:
        form = MessageForm()

    # 取引のメッセージを取得
    messages = transaction.messages.all()

    return render(request, 'mypage/transaction_chat.html', {'transaction': transaction, 'form': form, 'messages': messages})

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
