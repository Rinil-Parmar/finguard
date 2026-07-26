from django import forms
from django.core.exceptions import ValidationError

from .models import SavingsGoal


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'current_amount', 'target_date', 'notes', 'is_completed']
        labels = {
            'target_amount': 'Target amount (CAD)',
            'current_amount': 'Current saved amount (CAD)',
        }
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-finance-600 focus:ring-2 focus:ring-finance-100'
                })
        self.fields['is_completed'].widget.attrs.update({
            'class': 'h-4 w-4 rounded border-slate-300 text-finance-600 focus:ring-finance-600'
        })

    def clean(self):
        cleaned_data = super().clean()
        current_amount = cleaned_data.get('current_amount')
        target_amount = cleaned_data.get('target_amount')

        if current_amount is not None and target_amount is not None and current_amount > target_amount:
            raise ValidationError('Current saved amount cannot be greater than the target amount.')

        return cleaned_data
