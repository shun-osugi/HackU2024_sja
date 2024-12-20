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
from django.views.decorators.http import require_GET
import json

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'accounts/accoount.html')

def google_login(request):
    print("google_login")
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
            account_name = form.cleaned_data['account_name']  # account_nameを取得
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

            # Userオブジェクトの作成
            user = User.objects.create_user(username=account_name, email=email, password=password)

            user_profile = form.save(commit=False)
            user_profile.user = user  # UserProfileにUserを関連付ける
            user_profile.password = make_password(password)

            # 空き時間をJSON形式で保存
            availability_json = request.POST.get('availability', '[]')
            try:
                availability = json.loads(availability_json)
            except json.JSONDecodeError:
                availability = []  # デコードエラーの場合は空のリストを設定

            user_profile.availability = availability

            user_profile.save()
            messages.success(request, '登録が完了しました')
            return redirect('accounts:login')
        else:
            print(form.errors)  # フォームのエラーを出力
    else:
        form = UserProfileForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    user = request.user  # ログイン中のユーザーを取得
    try:
        user_profile = UserProfile.objects.get(user=user)  # ユーザープロファイルを取得
    except UserProfile.DoesNotExist:
        user_profile = None  # プロファイルが存在しない場合の処理

    return render(request, 'accounts/account.html', {'user_profile': user_profile})


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)  # ログイン成功
#             return redirect('home')
#         else:
#             # エラーメッセージを追加
#             messages.error(request, 'メールアドレスまたはパスワードが間違っています。')
#     return render(request, 'accounts/login.html')

@require_GET
def get_user_profile(request):
    print("User authenticated:", request.user.is_authenticated)  # デバッグ出力
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            print("User profile found:", user_profile.account_name)  # デバッグ出力
            response_data = {
                'isAuthenticated': True,
                'accountName': user_profile.account_name,
                'department': user_profile.department,
                'faculty': user_profile.faculty,
                'grade': user_profile.grade,
                'availability': user_profile.availability
            }
            print("Response data:", response_data)  # デバッグ出力
            return JsonResponse(response_data)
        except UserProfile.DoesNotExist as e:
            # エラーログを追加
            print(f"Profile not found for user {request.user.id}: {e}")
            response = JsonResponse({
                'isAuthenticated': True,
                'accountName': None,
                'department': None,
                'faculty': None,
                'grade': None,
                'availability': None
            })
    else:
        response = JsonResponse({
            'isAuthenticated': False,
            'accountName': None,
            'department': None,
            'faculty': None,
            'grade': None,
            'availability': None
        })

    response['Cache-Control'] = 'no-store, must-revalidate'
    return response