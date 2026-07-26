from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from transactions.models import Transaction

from .models import Budget


class BudgetViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='budget-user',
            password='test-password',
        )
        self.today = timezone.localdate()

    def test_budget_pages_require_login(self):
        for url_name in ('budget_detail', 'budget_set'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={reverse(url_name)}",
                )

    def test_detail_calculates_current_month_expenses(self):
        Budget.objects.create(
            user=self.user,
            month=self.today.month,
            year=self.today.year,
            amount=Decimal('500.00'),
        )
        Transaction.objects.create(
            user=self.user,
            title='Groceries',
            amount=Decimal('125.00'),
            transaction_type=Transaction.EXPENSE,
            category='groceries',
            date=self.today,
        )
        Transaction.objects.create(
            user=self.user,
            title='Salary',
            amount=Decimal('1000.00'),
            transaction_type=Transaction.INCOME,
            category='salary',
            date=self.today,
        )
        Transaction.objects.create(
            user=self.user,
            title='Previous expense',
            amount=Decimal('50.00'),
            transaction_type=Transaction.EXPENSE,
            category='other',
            date=self.today - timedelta(days=self.today.day),
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse('budget_detail'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthly_expenses'], Decimal('125.00'))
        self.assertEqual(response.context['remaining'], Decimal('375.00'))
        self.assertEqual(response.context['used_percent'], 25)

    def test_setting_budget_creates_current_user_budget(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('budget_set'), {
            'month': self.today.month,
            'year': self.today.year,
            'amount': '750.00',
        })

        self.assertRedirects(response, reverse('budget_detail'))
        budget = Budget.objects.get(user=self.user)
        self.assertEqual(budget.amount, Decimal('750.00'))

    def test_setting_current_budget_updates_instead_of_duplicating(self):
        budget = Budget.objects.create(
            user=self.user,
            month=self.today.month,
            year=self.today.year,
            amount=Decimal('500.00'),
        )
        self.client.force_login(self.user)

        response = self.client.post(reverse('budget_set'), {
            'month': self.today.month,
            'year': self.today.year,
            'amount': '900.00',
        })

        self.assertRedirects(response, reverse('budget_detail'))
        budget.refresh_from_db()
        self.assertEqual(budget.amount, Decimal('900.00'))
        self.assertEqual(Budget.objects.filter(user=self.user).count(), 1)
