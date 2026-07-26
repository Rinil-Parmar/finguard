from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from alerts.models import FraudAlert
from savings.models import SavingsGoal
from transactions.models import Transaction
from userhistory.models import UserActivity


class HomeView(TemplateView):
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.filter(user=self.request.user)
        income_total = transactions.filter(transaction_type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
        expense_total = transactions.filter(transaction_type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        active_savings_goals = SavingsGoal.objects.filter(user=self.request.user, is_completed=False)

        context.update({
            'income_total': income_total,
            'expense_total': expense_total,
            'balance': income_total - expense_total,
            'transaction_count': transactions.count(),
            'recent_transactions': transactions[:5],
            'open_alert_count': FraudAlert.objects.filter(user=self.request.user, is_resolved=False).count(),
            'recent_alerts': FraudAlert.objects.filter(user=self.request.user, is_resolved=False)[:3],
            'visit_count': self.request.session.get('visit_count', 0),
            'previous_visit': self.request.session.get('previous_visit'),
            'recent_activity': UserActivity.objects.filter(user=self.request.user).first(),
            'active_savings_count': active_savings_goals.count(),
            'next_savings_goal': active_savings_goals.first(),
        })
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'
