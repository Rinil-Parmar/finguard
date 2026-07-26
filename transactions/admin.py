from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'transaction_type', 'category', 'amount', 'date')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('title', 'notes', 'user__username')
