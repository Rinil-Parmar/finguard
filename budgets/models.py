from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    year = models.PositiveIntegerField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'month', 'year'],
                name='unique_user_monthly_budget',
            ),
        ]
        ordering = ['-year', '-month']

    def __str__(self):
        return f'{self.user.username} - {self.month}/{self.year} - CAD {self.amount}'

    @classmethod
    def current_month(cls):
        return timezone.localdate().month

    @classmethod
    def current_year(cls):
        return timezone.localdate().year
