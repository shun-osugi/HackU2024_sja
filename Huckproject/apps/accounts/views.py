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
            if request.POST['password'] != request.POST['password_confirm']:
                messages.error(request, 'パスワードが一致しません')
                return render(request, 'accounts/signup.html', {'form': form})

            # メールアドレスのドメイン確認
            email = form.cleaned_data['email']
            if not email.endswith('@ccmailg.meijo-u.ac.jp'):
                messages.error(request, '名城大学のメールアドレスを使用してください')
                return render(request, 'accounts/signup.html', {'form': form})
            # 重複アカウントのチェック
            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, 'このメールアドレスは既に登録されています')
                return render(request, 'accounts/signup.html', {'form': form})

            # ハッシュ化して保存
            user_profile = form.save(commit=False)
            user_profile.password = make_password(request.POST['password'])
            user_profile.save()
            user_profile = form.save(commit=False)
            user_profile.save()
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