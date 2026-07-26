from django.conf import settings
from django.db import models

from transactions.models import Transaction


class FraudAlert(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    SEVERITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fraud_alerts')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='fraud_alerts')
    reason = models.CharField(max_length=180)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default=MEDIUM)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_resolved', '-created_at']
        unique_together = ('transaction', 'reason')

    def __str__(self):
        return f'{self.get_severity_display()} alert for {self.transaction.title}'
