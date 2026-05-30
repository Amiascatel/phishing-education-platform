from django.contrib import admin
from .models import Badge, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sort_order', 'icon', 'requirement']
    list_editable = ['sort_order', 'category']
    list_filter = ['category']
    search_fields = ['name', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge__category']
    raw_id_fields = ['user']
    readonly_fields = ['earned_at']
