from django.contrib import admin
from .models import PhishingTemplate, Simulation, SimulationFeedback, SimulationCampaign


@admin.register(PhishingTemplate)
class PhishingTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'scenario', 'difficulty', 'is_active', 'created_at']
    list_filter = ['template_type', 'scenario', 'difficulty', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'subject', 'content']
    filter_horizontal = ['indicators']

    fieldsets = (
        (None, {
            'fields': ('name', 'template_type', 'scenario', 'difficulty', 'is_active')
        }),
        ('Email Settings', {
            'fields': ('sender_name', 'sender_email', 'subject'),
            'classes': ('collapse',),
        }),
        ('SMS Settings', {
            'fields': ('sender_number',),
            'classes': ('collapse',),
        }),
        ('Content', {
            'fields': ('content', 'html_content')
        }),
        ('Indicators', {
            'fields': ('indicators',)
        }),
    )


class SimulationFeedbackInline(admin.StackedInline):
    model = SimulationFeedback
    extra = 0
    readonly_fields = ['explanation', 'recommendations']


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'template', 'status', 'score', 'points_earned', 'started_at', 'completed_at']
    list_filter = ['status', 'template__template_type', 'template__scenario', 'user_identified_correctly']
    search_fields = ['user__username', 'template__name']
    readonly_fields = ['id', 'started_at', 'completed_at', 'score', 'time_spent_seconds']
    raw_id_fields = ['user', 'template']
    inlines = [SimulationFeedbackInline]

    fieldsets = (
        (None, {
            'fields': ('id', 'user', 'template', 'status')
        }),
        ('User Response', {
            'fields': ('user_clicked_link', 'user_submitted_data', 'user_reported', 'user_identified_correctly')
        }),
        ('Results', {
            'fields': ('score', 'points_earned', 'feedback')
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'time_spent_seconds')
        }),
    )


@admin.register(SimulationCampaign)
class SimulationCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'start_date', 'end_date', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['templates']
