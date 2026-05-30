from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, QuizResponse, AssessmentResult


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['text', 'is_correct', 'order']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['text', 'question_type', 'points', 'order']
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'quiz_type', 'module', 'passing_score', 'max_attempts', 'is_active']
    list_filter = ['quiz_type', 'is_active', 'module']
    list_editable = ['is_active', 'passing_score']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'quiz_type', 'module')
        }),
        ('Settings', {
            'fields': ('time_limit_minutes', 'passing_score', 'max_attempts', 'shuffle_questions', 'show_correct_answers', 'is_active')
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['quiz', 'question_type']
    list_editable = ['order', 'points']
    search_fields = ['text', 'quiz__title']
    inlines = [AnswerInline]

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question'

    fieldsets = (
        (None, {
            'fields': ('quiz', 'question_type', 'text', 'explanation')
        }),
        ('Settings', {
            'fields': ('points', 'order', 'image')
        }),
        ('Phishing Identification', {
            'fields': ('phishing_content', 'is_phishing'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    list_editable = ['is_correct', 'order']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Answer'


class QuizResponseInline(admin.TabularInline):
    model = QuizResponse
    extra = 0
    readonly_fields = ['question', 'selected_answer', 'is_correct']
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'percentage', 'passed', 'started_at', 'completed_at']
    list_filter = ['passed', 'quiz', 'quiz__quiz_type']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['started_at', 'completed_at', 'score', 'percentage', 'time_taken_seconds']
    raw_id_fields = ['user', 'quiz']
    inlines = [QuizResponseInline]


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'assessment_type', 'email_phishing_score', 'sms_phishing_score', 'created_at']
    list_filter = ['assessment_type']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
