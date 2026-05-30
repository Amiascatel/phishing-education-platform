from django.contrib import admin
from .models import (
    UserActivity, LearningAnalytics, PerformanceSnapshot,
    PlatformStatistics, AIRecommendation, UserFeedback
)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description_preview', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'description']
    readonly_fields = ['timestamp']
    raw_id_fields = ['user']

    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'


@admin.register(LearningAnalytics)
class LearningAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'modules_completed', 'quizzes_completed', 'simulations_completed', 'average_quiz_score', 'login_count']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']

    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Time Metrics', {
            'fields': ('total_time_spent', 'average_session_duration', 'last_activity')
        }),
        ('Completion Metrics', {
            'fields': ('modules_completed', 'quizzes_completed', 'simulations_completed')
        }),
        ('Performance Metrics', {
            'fields': ('average_quiz_score', 'average_simulation_score', 'improvement_rate')
        }),
        ('Engagement Metrics', {
            'fields': ('login_count', 'streak_days', 'longest_streak')
        }),
    )


@admin.register(PerformanceSnapshot)
class PerformanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'overall_score', 'email_phishing_score', 'sms_phishing_score', 'total_points']
    list_filter = ['date']
    search_fields = ['user__username']
    date_hierarchy = 'date'


@admin.register(PlatformStatistics)
class PlatformStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_users', 'active_users', 'new_registrations', 'total_logins', 'phishing_detection_rate']
    date_hierarchy = 'date'
    readonly_fields = ['date']


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation_type', 'title', 'priority', 'is_dismissed', 'created_at']
    list_filter = ['recommendation_type', 'is_dismissed', 'priority']
    list_editable = ['is_dismissed']
    search_fields = ['user__username', 'title', 'description']
    raw_id_fields = ['user', 'related_module']


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'feedback_type', 'subject', 'rating', 'is_resolved', 'created_at']
    list_filter = ['feedback_type', 'is_resolved', 'rating']
    list_editable = ['is_resolved']
    search_fields = ['user__username', 'subject', 'message']
    readonly_fields = ['created_at']

    fieldsets = (
        (None, {
            'fields': ('user', 'feedback_type', 'subject', 'message', 'rating')
        }),
        ('Related Items', {
            'fields': ('related_module', 'related_simulation'),
            'classes': ('collapse',)
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'admin_response')
        }),
    )
