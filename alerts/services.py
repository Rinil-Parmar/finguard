from decimal import Decimal

from django.db.models import Avg

from transactions.models import Transaction

from .models import FraudAlert

LARGE_EXPENSE_LIMIT = Decimal('1000.00')
AVERAGE_MULTIPLIER = Decimal('3')


def analyze_transaction(transaction):
    if transaction.transaction_type != Transaction.EXPENSE:
        transaction.fraud_alerts.update(is_resolved=True)
        return []

    active_reasons = []
    checks = [
        _large_expense_check(transaction),
        _duplicate_expense_check(transaction),
        _above_average_check(transaction),
    ]

    for check in checks:
        if check:
            reason, severity = check
            active_reasons.append(reason)
            FraudAlert.objects.update_or_create(
                transaction=transaction,
                reason=reason,
                defaults={
                    'user': transaction.user,
                    'severity': severity,
                    'is_resolved': False,
                },
            )

    transaction.fraud_alerts.exclude(reason__in=active_reasons).update(is_resolved=True)
    return active_reasons


def _large_expense_check(transaction):
    if transaction.amount >= LARGE_EXPENSE_LIMIT:
        return ('Expense amount is CAD 1000.00 or higher.', FraudAlert.HIGH)
    return None


def _duplicate_expense_check(transaction):
    exists = Transaction.objects.filter(
        user=transaction.user,
        title__iexact=transaction.title,
        amount=transaction.amount,
        date=transaction.date,
        transaction_type=Transaction.EXPENSE,
    ).exclude(pk=transaction.pk).exists()

    if exists:
        return ('Possible duplicate expense with the same title, amount, and date.', FraudAlert.MEDIUM)
    return None


def _above_average_check(transaction):
    average = Transaction.objects.filter(
        user=transaction.user,
        transaction_type=Transaction.EXPENSE,
        amount__lt=LARGE_EXPENSE_LIMIT,
    ).exclude(pk=transaction.pk).aggregate(value=Avg('amount'))['value']

    if average and transaction.amount > average * AVERAGE_MULTIPLIER:
        return ('Expense is more than three times your average expense.', FraudAlert.MEDIUM)
    return None
