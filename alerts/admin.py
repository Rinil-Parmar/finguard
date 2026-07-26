from django.contrib import admin

from .models import FraudAlert


@admin.register(FraudAlert)
class FraudAlertAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'user', 'severity', 'is_resolved', 'created_at')
    list_filter = ('severity', 'is_resolved', 'created_at')
    search_fields = ('transaction__title', 'reason', 'user__username')
