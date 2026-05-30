from django.db import models
from django.conf import settings


class Quiz(models.Model):
    """Quiz for testing phishing awareness."""

    QUIZ_TYPE_CHOICES = [
        ('pre_assessment', 'Pre-Assessment'),
        ('post_assessment', 'Post-Assessment'),
        ('module_quiz', 'Module Quiz'),
        ('practice', 'Practice Quiz'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES)
    module = models.ForeignKey(
        'education.Module', on_delete=models.CASCADE,
        related_name='quizzes', null=True, blank=True
    )
    time_limit_minutes = models.IntegerField(default=2)
    passing_score = models.FloatField(default=70.0)
    max_attempts = models.IntegerField(default=3)
    shuffle_questions = models.BooleanField(default=True)
    show_correct_answers = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

    def get_total_points(self):
        return sum(q.points for q in self.questions.all())


class Question(models.Model):
    """Question for a quiz."""

    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('identify_phishing', 'Identify Phishing'),
        ('spot_indicators', 'Spot Indicators'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    text = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    # For phishing identification questions
    phishing_content = models.TextField(blank=True)
    is_phishing = models.BooleanField(null=True, blank=True)

    # Image support
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}"


class Answer(models.Model):
    """Answer option for a question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.text[:50]} ({'Correct' if self.is_correct else 'Incorrect'})"


class QuizAttempt(models.Model):
    """User's attempt at a quiz."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

    def calculate_score(self):
        """Calculate score from user responses."""
        total_points = self.quiz.get_total_points()
        earned_points = sum(
            r.question.points for r in self.responses.filter(is_correct=True)
        )
        self.points_earned = earned_points
        self.score = earned_points
        self.percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        self.passed = self.percentage >= self.quiz.passing_score
        return self.percentage


class QuizResponse(models.Model):
    """User's response to a quiz question."""

    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    text_response = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken_seconds = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"Response to {self.question}"

    def check_answer(self):
        """Check if the response is correct."""
        if self.question.question_type in ['multiple_choice', 'true_false']:
            if self.selected_answer:
                self.is_correct = self.selected_answer.is_correct
        elif self.question.question_type == 'identify_phishing':
            user_says_phishing = self.text_response.lower() == 'phishing'
            self.is_correct = user_says_phishing == self.question.is_phishing
        self.save()
        return self.is_correct


class AssessmentResult(models.Model):
    """Summary of pre/post assessment results."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_results')
    assessment_type = models.CharField(max_length=20)
    quiz_attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE)

    # Score breakdown by category
    email_phishing_score = models.FloatField(default=0)
    sms_phishing_score = models.FloatField(default=0)
    social_engineering_score = models.FloatField(default=0)
    general_awareness_score = models.FloatField(default=0)

    # Analysis
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.assessment_type}"
