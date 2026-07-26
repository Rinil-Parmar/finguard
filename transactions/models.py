from django.conf import settings
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('salary', 'Salary'),
        ('rent', 'Rent'),
        ('groceries', 'Groceries'),
        ('shopping', 'Shopping'),
        ('travel', 'Travel'),
        ('bills', 'Bills'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField(default=timezone.localdate)
    notes = models.TextField(blank=True)
    receipt = models.FileField(
        upload_to='receipts/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.title} - CAD {self.amount}'

    def get_absolute_url(self):
        return reverse('transaction_list')
