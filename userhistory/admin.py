from django.contrib import admin

from .models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'page_name', 'method', 'timestamp')
    list_filter = ('method', 'timestamp')
    search_fields = ('user__username', 'path', 'page_name')
