from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from transactions.models import Transaction


def home(request):
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    income_total = transactions.filter(transaction_type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
    expense_total = transactions.filter(transaction_type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    balance = income_total - expense_total
    recent_transactions = transactions[:5]

    context = {
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'transaction_count': transactions.count(),
        'recent_transactions': recent_transactions,
    }
    return render(request, 'core/dashboard.html', context)
