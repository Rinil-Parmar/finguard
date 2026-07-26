from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    income_total = sum(item.amount for item in transactions if item.transaction_type == Transaction.INCOME)
    expense_total = sum(item.amount for item in transactions if item.transaction_type == Transaction.EXPENSE)
    balance = income_total - expense_total

    context = {
        'transactions': transactions,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
    }
    return render(request, 'transactions/transaction_list.html', context)


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'transactions/transaction_form.html', {
        'form': form,
        'page_title': 'Add transaction',
        'button_label': 'Save transaction',
    })


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transactions/transaction_form.html', {
        'form': form,
        'page_title': 'Edit transaction',
        'button_label': 'Update transaction',
    })


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction,
    })
