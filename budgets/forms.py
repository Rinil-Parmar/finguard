import calendar

from django import forms
from django.utils import timezone

from .models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'year', 'amount']
        labels = {
            'amount': 'Monthly budget amount (CAD)',
        }
        widgets = {
            'month': forms.Select(
                choices=[(month, calendar.month_name[month]) for month in range(1, 13)],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].initial = timezone.localdate().year

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-finance-600 focus:ring-2 focus:ring-finance-100',
            })
