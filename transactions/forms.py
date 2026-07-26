from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Transaction

MAX_RECEIPT_SIZE = 5 * 1024 * 1024


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category', 'date', 'notes', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'amount': 'Amount (CAD)',
            'receipt': 'Receipt or document',
        }
        help_texts = {
            'receipt': 'Optional. Upload PDF, JPG, JPEG, or PNG files up to 5 MB.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = timezone.localdate()

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-finance-600 focus:ring-2 focus:ring-finance-100'
            })

    def clean_date(self):
        transaction_date = self.cleaned_data['date']
        if transaction_date > timezone.localdate():
            raise ValidationError('Transaction date cannot be in the future.')
        return transaction_date

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt and receipt.size > MAX_RECEIPT_SIZE:
            raise ValidationError('Receipt file must be 5 MB or smaller.')
        return receipt
