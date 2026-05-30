from django.db import models
from django.conf import settings


class AdaptiveQuestion(models.Model):
    """Quiz question with IRT parameters for the adaptive quiz system."""

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    category = models.ForeignKey(
        'education.Category', on_delete=models.CASCADE,
        related_name='adaptive_questions'
    )
    question = models.TextField()
    scenario = models.TextField(blank=True, null=True)
    # JSON array of 4 strings: ["Option A", "Option B", "Option C", "Option D"]
    options = models.JSONField()
    # Integer 0-3 index into options array
    correct_answer = models.IntegerField()
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    # IRT parameters
    discrimination_index = models.FloatField(default=1.0, null=True, blank=True)
    difficulty_parameter = models.FloatField(default=0.0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_questions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'difficulty']

    def __str__(self):
        return f"[{self.category.name}] {self.question[:60]}"

    def get_correct_option_text(self):
        try:
            return self.options[self.correct_answer]
        except (IndexError, TypeError):
            return ''


class AdaptiveQuizAttempt(models.Model):
    """User attempt at a category-based adaptive quiz."""

    QUIZ_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('adaptive', 'Adaptive'),
        ('pre_test', 'Pre-Test'),
        ('post_test', 'Post-Test'),
    ]
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='adaptive_quiz_attempts'
    )
    category = models.ForeignKey(
        'education.Category', on_delete=models.CASCADE,
        null=True, blank=True, related_name='quiz_attempts'
    )
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES, default='adaptive')
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    score_percentage = models.FloatField(null=True, blank=True)
    estimated_level = models.CharField(max_length=20, blank=True, null=True)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    difficulty_progression = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        cat = self.category.name if self.category else 'Mixed'
        return f"{self.user.username} - {cat} ({self.quiz_type})"


class AdaptiveQuizAnswer(models.Model):
    """Single answer within an adaptive quiz attempt."""

    attempt = models.ForeignKey(
        AdaptiveQuizAttempt, on_delete=models.CASCADE, related_name='answers'
    )
    question = models.ForeignKey(
        AdaptiveQuestion, on_delete=models.CASCADE, related_name='quiz_answers'
    )
    selected_answer = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    question_order = models.IntegerField(default=0)

    class Meta:
        unique_together = ['attempt', 'question']
        ordering = ['question_order']

    def __str__(self):
        return f"Answer {self.question_order} for attempt {self.attempt_id}"


class UserKnowledgeProfile(models.Model):
    """Bayesian IRT-estimated knowledge level per user per category."""

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='knowledge_profiles'
    )
    category = models.ForeignKey(
        'education.Category', on_delete=models.CASCADE,
        related_name='knowledge_profiles'
    )
    estimated_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    proficiency_score = models.FloatField(default=0.3)
    confidence = models.FloatField(default=0.1)
    total_questions_answered = models.IntegerField(default=0)
    correct_answers_count = models.IntegerField(default=0)
    last_assessed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'category']

    def __str__(self):
        return f"{self.user.username} - {self.category.name}: {self.estimated_level}"


class AdminContentSubmission(models.Model):
    """Admin-submitted content to feed to ML models."""

    CONTENT_TYPES = [
        ('chatbot_qa', 'Chatbot Q&A Pair'),
        ('question', 'Quiz Question'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    content_type = models.CharField(max_length=30, choices=CONTENT_TYPES)
    content_data = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    fed_to_model = models.BooleanField(default=False)
    fed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type} by {self.submitted_by}"
