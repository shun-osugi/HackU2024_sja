# views.py (transactionsアプリ)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaction, Message
from .forms import MessageForm, MeetingTimeForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def transaction_chat(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    messages = transaction.messages.all().order_by('timestamp')

    form = MessageForm()  # 初期化
    time_form = MeetingTimeForm(instance=transaction)  # 初期化

    if request.method == 'POST':
        if 'send_message' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.transaction = transaction
                message.sender = request.user
                message.save()
                return redirect('transaction_chat', pk=transaction.pk)
        elif 'send_time' in request.POST:
            time_form = MeetingTimeForm(request.POST, instance=transaction)
            if time_form.is_valid():
                time_form.save()
                return redirect('transaction_chat', pk=transaction.pk)
        elif 'cancel_transaction' in request.POST and request.user == transaction.seller:
            transaction.status = 'cancelled'
            transaction.save()
            return redirect('transaction_chat', pk=transaction.pk)
        elif 'approve_transaction' in request.POST and request.user == transaction.seller:
            transaction.status = 'completed'
            transaction.save()
            return redirect('transaction_chat', pk=transaction.pk)

    return render(request, 'transactions/transaction_chat.html', {
        'transaction': transaction,
        'messages': messages,
        'form': form,
        'time_form': time_form
    })

@login_required
def transaction_list(request):
    # ログインユーザーが「売り手」または「買い手」で、ステータスが「pending」の取引を取得
    transactions = Transaction.objects.filter(
        Q(seller=request.user) | Q(buyer=request.user),
        status='pending'
    )

    # 商品リストを作成
    products = [transaction.product for transaction in transactions]

    return render(request, 'transactions/transaction_list.html', {'products': products})