from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.products.models import UserProfile
from .forms import UserProfileForm
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'accounts/accoount.html')

def google_login(request):
    if request.method == 'GET':
        # GETリクエストの場合はログインページを表示
        return render(request, 'accounts/login.html')
        
    elif request.method == 'POST':
        # メールアドレスとパスワードを使用してログイン
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'メールアドレスとパスワードを入力してください')
            return render(request, 'accounts/login.html')

        # ユーザーの認証
        try:
            user_profile = UserProfile.objects.get(email=email)
            if user_profile.check_password(password):
                # ログイン成功時の処理
                return redirect('home')
            else:
                messages.error(request, 'パスワードが間違っています')
                return render(request, 'accounts/login.html')
        except UserProfile.DoesNotExist:
            messages.error(request, 'ユーザーが見つかりません')
            return render(request, 'accounts/login.html')

    # その他のHTTPメソッドの場合
    return JsonResponse({'error': '不正なリクエストメソッドです'}, status=405)

def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # パスワード確認
            password = form.cleaned_data.get('password')
            password_confirm = request.POST.get('password_confirm')
            if password != password_confirm:
                messages.error(request, 'パスワードが一致しません')
                return render(request, 'accounts/signup.html', {'form': form})

            # メールアドレスのドメイン確認
            email = form.cleaned_data['email']
            if not email.endswith('@ccmailg.meijo-u.ac.jp'):
                messages.error(request, '名城大学のメールアドレスを使用してください')
                return render(request, 'accounts/signup.html', {'form': form})

            # ユーザー名の重複チェック
            username = form.cleaned_data.get('account_name')
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, 'このユーザー名は既に使用されています')
                return render(request, 'accounts/signup.html', {'form': form})

            # 重複アカウントのチェック
            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, 'このメールアドレスは既に登録されています')
                return render(request, 'accounts/signup.html', {'form': form})

            # ユーザーを保存
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            logger.debug(f"User created: {user}")

            # ユーザープロファイルを作成し、user_idを設定
            user_profile = UserProfile(
                user=user,
                account_name=username,
                email=email,
                department=form.cleaned_data.get('department'),
                password=password
            )
            user_profile.save()

            logger.debug(f"UserProfile created: {user_profile}")

            messages.success(request, '登録が完了しました')
            return redirect('accounts:login')
    else:
        form = UserProfileForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # ログイン成功
            login(request, user)
            return redirect('home')
        else:
            # エラーメッセージを追加
            messages.error(request, 'メールアドレスまたはパスワードが間違っています。')
    return render(request, 'accounts/login.html')