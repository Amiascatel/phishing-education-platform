from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProgress, LearningPath


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'skill_level', 'total_points', 'completed_modules', 'is_active']
    list_filter = ['skill_level', 'is_active', 'pre_assessment_completed', 'post_assessment_completed']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-total_points']

    fieldsets = UserAdmin.fieldsets + (
        ('Learning Profile', {
            'fields': ('phone_number', 'profile_picture', 'skill_level', 'total_points', 'completed_modules')
        }),
        ('Phishing Scores', {
            'fields': ('email_phishing_score', 'sms_phishing_score', 'social_engineering_score')
        }),
        ('Assessment Status', {
            'fields': ('pre_assessment_completed', 'pre_assessment_score', 'post_assessment_completed', 'post_assessment_score')
        }),
    )

    readonly_fields = ['total_points', 'completed_modules', 'email_phishing_score', 'sms_phishing_score', 'social_engineering_score']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'completed', 'score', 'attempts', 'completion_date']
    list_filter = ['completed', 'module__category', 'module__difficulty']
    search_fields = ['user__username', 'module__title']
    raw_id_fields = ['user', 'module']


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['user', 'focus_area', 'created_at', 'updated_at']
    list_filter = ['focus_area']
    search_fields = ['user__username']
    filter_horizontal = ['recommended_modules']
