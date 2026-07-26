from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=120)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    target_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_completed', 'target_date', '-created_at']

    def __str__(self):
        return f'{self.name} - CAD {self.current_amount} / CAD {self.target_amount}'

    @property
    def progress_percent(self):
        if self.target_amount <= 0:
            return 0
        return min(round((self.current_amount / self.target_amount) * 100), 100)

    @property
    def remaining_amount(self):
        return max(self.target_amount - self.current_amount, 0)

    @property
    def is_overdue(self):
        return bool(self.target_date and self.target_date < timezone.localdate() and not self.is_completed)

    def get_absolute_url(self):
        return reverse('savings_goal_list')
