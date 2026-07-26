from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from transactions.models import Transaction

from .forms import BudgetForm
from .models import Budget


@login_required
def budget_detail(request):
    today = timezone.localdate()
    budget = Budget.objects.filter(
        user=request.user,
        month=today.month,
        year=today.year,
    ).first()
    monthly_expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type=Transaction.EXPENSE,
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    budget_amount = budget.amount if budget else Decimal('0.00')
    remaining = budget_amount - monthly_expenses
    used_percent = 0
    if budget_amount > 0:
        used_percent = min(round((monthly_expenses / budget_amount) * 100), 100)

    return render(request, 'budgets/budget_detail.html', {
        'budget': budget,
        'monthly_expenses': monthly_expenses,
        'remaining': remaining,
        'used_percent': used_percent,
        'month': today.strftime('%B'),
        'year': today.year,
    })


@login_required
def budget_set(request):
    today = timezone.localdate()
    budget = Budget.objects.filter(
        user=request.user,
        month=today.month,
        year=today.year,
    ).first()

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            submitted_budget = form.save(commit=False)
            submitted_budget.user = request.user
            submitted_budget.save()
            return redirect('budget_detail')
    else:
        form = BudgetForm(
            instance=budget,
            initial={'month': today.month, 'year': today.year},
        )

    return render(request, 'budgets/budget_form.html', {'form': form})
