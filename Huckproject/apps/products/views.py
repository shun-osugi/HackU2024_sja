from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Product, Comment, Favorite,UserProfile
from .forms import ProductFilterForm
from django.db.models import Q
from openjij import SQASampler
import numpy as np
import logging  # ログ出力用

# ロガーの設定
logger = logging.getLogger(__name__)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
@require_POST
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    content = request.POST.get('content')
    comment = Comment.objects.create(product=product, user=request.user, content=content)
    return JsonResponse({
        'username': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@login_required
@require_POST
def toggle_favorite(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    # お気に入りを作成または削除
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
    
    return JsonResponse({'is_favorite': created})

@login_required
def favorite_list(request):
    # 現在ログインしているユーザーのお気に入り商品を取得
    favorites = Favorite.objects.filter(user=request.user)
    
    # お気に入り商品をリスト化
    products = [favorite.product for favorite in favorites]

    return render(request, 'favorite.html', {'products': products})

def transaction_page(request, product_id):
    return render(request, 'transaction_page.html', {'product_id': product_id})

def product_list(request):
    form = ProductFilterForm(request.GET)  # フォームのインスタンス化
    products = Product.objects.all()

    # ソート処理
    sort_by = request.GET.get('sort', 'name')  # デフォルトは名前でソート
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')

    # 検索処理
    query = request.GET.get('q')  # 検索クエリを取得
    if query:
        products = products.filter(Q(name__icontains=query))  # 商品名で検索

    # フィルタリング処理
    if form.is_valid():  # フォームが有効かどうかをチェック
        grade = form.cleaned_data['grade']
        faculty = form.cleaned_data['faculty']
        department = form.cleaned_data['department']
        show_favorites = form.cleaned_data.get('show_favorites')

        if grade and int(grade) != 0:
            products = products.filter(grade=grade)
        if faculty:
            products = products.filter(faculty=faculty)
        if department:
            products = products.filter(department=department)
        
        # お気に入りのフィルタリング
        if show_favorites and request.user.is_authenticated:
            favorite_products = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
            products = products.filter(id__in=favorite_products)

    # ============================================
    # 量子アニーリングによる空き時間マッチング処理
    # ============================================
    matching_result = None  # 結果を格納する変数
    
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user=request.user)
        current_availability = current_user.availability

        # 他のユーザーの空き時間を取得
        other_users = UserProfile.objects.exclude(user=request.user)
        other_availabilities = [(user.account_name, user.availability) for user in other_users]

        def calculate_energy(schedule1, schedule2):
            """2人のスケジュールの一致度に基づいたエネルギーを計算"""
            energy = 0
            for i in range(5):  # 月〜金
                for j in range(6):  # 1限〜6限
                    if schedule1[i][j] == 1 and schedule2[i][j] == 1:  # 両者の空き時間が一致
                        energy -= 1  # 一致する空き時間が多いほどエネルギーが小さくなる
                        
                        # 予定があるコマに挟まれた空き時間の比重を重くする
                        if j > 0 and schedule1[i][j-1] == 0 and schedule1[i][j+1] == 0:
                            energy -= 2  # 空き時間が予定のある時間に挟まれている場合、重みを加える（例：3倍）

                        # 連続した空き時間に対して価値を0.7倍する
                        if j < 5 and schedule1[i][j] == 1 and schedule1[i][j+1] == 1:
                            energy *= 0.7  # 連続した空き時間の価値を0.7倍にする
            return energy

        # QUBO行列の作成
        n_users = len(other_availabilities)
        qubo_matrix = np.zeros((n_users, n_users))

        for idx, (_, avail) in enumerate(other_availabilities):
            qubo_matrix[idx, idx] = calculate_energy(current_availability, avail)

        # エネルギーを計算してログに出力
        energies = []  # 全員のエネルギーを格納するリスト
        for idx, (name, avail) in enumerate(other_availabilities):
            energy = calculate_energy(current_availability, avail)
            qubo_matrix[idx, idx] = energy
            energies.append((name, energy))
            logger.info(f"User: {name}, Energy: {energy}")  # エネルギーのログ出力

        # OpenJijを使って最適な解を求める
        sampler = SQASampler()
        response = sampler.sample_qubo(qubo_matrix)
        best_match_index = np.argmin(response.energies)  # 最小エネルギーのインデックス

        # QUBO行列からエネルギーを抽出
        diagonal_energies = [qubo_matrix[i, i] for i in range(len(qubo_matrix))]

        # 最小エネルギーのインデックスを取得
        best_match_index = diagonal_energies.index(min(diagonal_energies))

        # 最適な相手を取得
        matching_result = other_availabilities[best_match_index][0]

        # 結果を出力
        print(f"Best Match: {matching_result}")

        # 全員のエネルギーをコンソールに表示（デバッグ用）
        print("=== User Energies ===")
        for name, energy in energies:
            print(f"{name}: {energy}")
        print("=====================")

    context = {
        'form': form,
        'products': products,
        'query': query,
        'matching_result': matching_result,  # マッチング結果をテンプレートに渡す
    }
    
    return render(request, 'products/product_list.html', context)
