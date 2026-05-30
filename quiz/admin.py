from django.contrib import admin
from django.utils import timezone
from .models import (
    AdaptiveQuestion, AdaptiveQuizAttempt, AdaptiveQuizAnswer,
    UserKnowledgeProfile, AdminContentSubmission
)


@admin.register(AdaptiveQuestion)
class AdaptiveQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'difficulty', 'difficulty_parameter', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active']
    list_editable = ['is_active', 'difficulty']
    search_fields = ['question', 'explanation']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['activate_questions', 'deactivate_questions']

    def question_preview(self, obj):
        return obj.question[:80]
    question_preview.short_description = 'Question'

    def activate_questions(self, request, queryset):
        queryset.update(is_active=True)
    activate_questions.short_description = 'Activate selected questions'

    def deactivate_questions(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_questions.short_description = 'Deactivate selected questions'


@admin.register(AdaptiveQuizAttempt)
class AdaptiveQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'quiz_type', 'score_percentage', 'estimated_level', 'status', 'completed_at']
    list_filter = ['quiz_type', 'status', 'estimated_level', 'category']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(UserKnowledgeProfile)
class UserKnowledgeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'estimated_level', 'proficiency_score', 'confidence', 'total_questions_answered']
    list_filter = ['estimated_level', 'category']
    search_fields = ['user__username']
    readonly_fields = ['last_assessed_at']


@admin.register(AdminContentSubmission)
class AdminContentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'submitted_by', 'status', 'fed_to_model', 'created_at']
    list_filter = ['content_type', 'status', 'fed_to_model']
    readonly_fields = ['created_at', 'fed_at']
    actions = ['approve_and_feed_to_model']

    def approve_and_feed_to_model(self, request, queryset):
        from ml_engine.models.chatbot import chatbot as chatbot_model
        chatbot_submissions = queryset.filter(
            content_type='chatbot_qa', status='approved', fed_to_model=False
        )
        new_pairs = [s.content_data for s in chatbot_submissions]
        if new_pairs:
            chatbot_model.add_qa_pairs(new_pairs)
            chatbot_submissions.update(fed_to_model=True, fed_at=timezone.now(), status='approved')
            self.message_user(request, f'Fed {len(new_pairs)} Q&A pairs to the chatbot model.')
        else:
            self.message_user(request, 'No approved chatbot Q&A submissions to feed.')
    approve_and_feed_to_model.short_description = 'Approve & feed selected items to ML model'
