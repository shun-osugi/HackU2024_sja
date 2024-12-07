from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Listing
from django.views.decorators.http import require_POST

def create_listing(request):
    if request.method == 'POST':
        # フォームからのデータを取得
        product_name = request.POST.get('product_name')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        price = request.POST.get('price')
        faculty = request.POST.get('faculty')
        department = request.POST.get('department')
        image = request.FILES.get('image')  # ファイルはFILESから取得

        # データ保存
        listing = Listing(
            product_name=product_name,
            subject=subject,
            description=description,
            price=price,
            faculty=faculty,
            department=department,
            image=image
        )
        listing.save()

        # どのボタンが押されたかを判定
        action = request.POST.get('action')
        if action == 'draft':#下書きどうする？
            return redirect("listings:listing")
        else:
            return redirect("listings:listing")

    # GETリクエストの場合、フォームページを表示
    return render(request, 'listings/listing.html')
