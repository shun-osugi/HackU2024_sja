from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Product, Comment, Favorite
from .forms import ProductFilterForm
from django.db.models import F
from django.db.models import Q  

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

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
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
    
    return JsonResponse({'is_favorite': created})

def transaction_page(request, product_id):
    # トランザクションページの処理を実装
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
        # descriptionフィールドが存在するか確認し、存在しない場合は商品名だけでフィルタリング
        products = products.filter(Q(name__icontains=query))  # 商品名で検索

    # フィルタリング処理
    if form.is_valid():  # フォームが有効かどうかをチェック
        grade = form.cleaned_data['grade']
        faculty = form.cleaned_data['faculty']
        department = form.cleaned_data['department']

        if grade and int(grade) != 0:
            products = products.filter(grade=grade)
        if faculty:
            products = products.filter(faculty=faculty)
        if department:
            products = products.filter(department=department)

    context = {
        'form': form,  # コンテキストにフォームを追加
        'products': products,
        'query': query,  # 検索クエリをコンテキストに追加
    }
    
    
    
    return render(request, 'products/product_list.html', context)