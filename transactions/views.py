from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from alerts.services import analyze_transaction

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    query = request.GET.get('q', '').strip()
    transaction_type = request.GET.get('type', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        transactions = transactions.filter(
            Q(title__icontains=query)
            | Q(notes__icontains=query)
            | Q(category__icontains=query)
        )

    if transaction_type in [Transaction.INCOME, Transaction.EXPENSE]:
        transactions = transactions.filter(transaction_type=transaction_type)

    valid_categories = [choice[0] for choice in Transaction.CATEGORY_CHOICES]
    if category in valid_categories:
        transactions = transactions.filter(category=category)

    income_total = sum(item.amount for item in transactions if item.transaction_type == Transaction.INCOME)
    expense_total = sum(item.amount for item in transactions if item.transaction_type == Transaction.EXPENSE)
    balance = income_total - expense_total

    context = {
        'transactions': transactions,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'query': query,
        'selected_type': transaction_type,
        'selected_category': category,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'categories': Transaction.CATEGORY_CHOICES,
        'has_filters': bool(query or transaction_type or category),
    }
    return render(request, 'transactions/transaction_list.html', context)


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            try:
                transaction.save()
            except (OSError, SuspiciousOperation):
                form.add_error('receipt', 'Receipt upload failed. Try a smaller PDF or upload JPG/PNG instead.')
                return render(request, 'transactions/transaction_form.html', {
                    'form': form,
                    'page_title': 'Add transaction',
                    'button_label': 'Save transaction',
                })
            analyze_transaction(transaction)
            messages.success(request, 'Transaction added successfully.')
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
            try:
                transaction = form.save()
            except (OSError, SuspiciousOperation):
                form.add_error('receipt', 'Receipt upload failed. Try a smaller PDF or upload JPG/PNG instead.')
                return render(request, 'transactions/transaction_form.html', {
                    'form': form,
                    'page_title': 'Edit transaction',
                    'button_label': 'Update transaction',
                })
            analyze_transaction(transaction)
            messages.success(request, 'Transaction updated successfully.')
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
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('transaction_list')

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction,
    })
