from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.products.models import UserProfile
from .forms import UserProfileForm
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'accounts/accoount.html')

def google_login(request):
    if request.method == 'GET':
        # GETリクエストの場合はログインページを表示
        return render(request, 'accounts/login.html')
        
    elif request.method == 'POST':
        try:
            # トークンをリクエストから取得
            token = request.POST.get('id_token')
            if not token:
                return JsonResponse({'error': 'トークンが見つかりません'}, status=400)

            # Googleからのトークン検証
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(),
                '967268568153-u26ndg6fo080hkrstdo5chtgvdj8u3ha.apps.googleusercontent.com'
            )
            
            # メールアドレスの検証
            email = idinfo['email']
            if not email.endswith('@ccmailg.meijo-u.ac.jp'):
                return JsonResponse({'error': '許可されていないメールドメインです'})
                
            # メールアドレスの形式チェック（9桁の数字）
            account_number = email.split('@')[0]
            if not (account_number.isdigit() and len(account_number) == 9):
                return JsonResponse({'error': '無効なアカウント番号です'})
            # ユーザーが存在するか確認し、存在しない場合は作成
            user_profile, created = UserProfile.objects.get_or_create(
                email=email,
                defaults={
                    'account_name': account_number,  # 必要に応じて名前を設定
                }
            )
            # ログイン成功時の処理
            return JsonResponse({'success': True, 'created': created})

        except ValueError as e:
            return JsonResponse({'error': '無効なトークンです'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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