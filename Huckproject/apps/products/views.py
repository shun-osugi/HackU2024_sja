from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Product, Comment, Favorite
from .forms import ProductFilterForm
from django.db.models import Q

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product).order_by('-created_at')
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'comments': comments,
        'is_favorite': is_favorite
    })

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

    context = {
        'form': form,
        'products': products,
        'query': query,
    }
    
    return render(request, 'products/product_list.html', context)
