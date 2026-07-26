from django.contrib import admin

from .models import SavingsGoal


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'current_amount', 'target_amount', 'target_date', 'is_completed')
    list_filter = ('is_completed', 'target_date')
    search_fields = ('name', 'notes', 'user__username')
