from django.db import models
from django.conf import settings


class UserActivity(models.Model):
    """Track user activities on the platform."""

    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('module_start', 'Module Started'),
        ('module_complete', 'Module Completed'),
        ('quiz_start', 'Quiz Started'),
        ('quiz_complete', 'Quiz Completed'),
        ('simulation_start', 'Simulation Started'),
        ('simulation_complete', 'Simulation Completed'),
        ('resource_view', 'Resource Viewed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"


class LearningAnalytics(models.Model):
    """Aggregated learning analytics for a user."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_analytics')

    # Time metrics
    total_time_spent = models.DurationField(null=True, blank=True)
    average_session_duration = models.DurationField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    # Completion metrics
    modules_completed = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    simulations_completed = models.IntegerField(default=0)

    # Performance metrics
    average_quiz_score = models.FloatField(default=0)
    average_simulation_score = models.FloatField(default=0)
    improvement_rate = models.FloatField(default=0)

    # Engagement metrics
    login_count = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Learning Analytics'

    def __str__(self):
        return f"Analytics for {self.user.username}"


class PerformanceSnapshot(models.Model):
    """Periodic snapshot of user performance for trend analysis."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_snapshots')
    date = models.DateField()

    # Scores at this point in time
    overall_score = models.FloatField()
    email_phishing_score = models.FloatField()
    sms_phishing_score = models.FloatField()
    social_engineering_score = models.FloatField()

    # Cumulative metrics
    total_points = models.IntegerField()
    modules_completed = models.IntegerField()

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class PlatformStatistics(models.Model):
    """Platform-wide statistics for admin dashboard."""

    date = models.DateField(unique=True)

    # User metrics
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    new_registrations = models.IntegerField(default=0)

    # Engagement metrics
    total_logins = models.IntegerField(default=0)
    modules_started = models.IntegerField(default=0)
    modules_completed = models.IntegerField(default=0)
    quizzes_taken = models.IntegerField(default=0)
    simulations_run = models.IntegerField(default=0)

    # Performance metrics
    average_quiz_score = models.FloatField(default=0)
    average_simulation_score = models.FloatField(default=0)
    phishing_detection_rate = models.FloatField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Platform Stats - {self.date}"


class AIRecommendation(models.Model):
    """AI-generated recommendations for users."""

    RECOMMENDATION_TYPE_CHOICES = [
        ('module', 'Module Recommendation'),
        ('practice', 'Practice Recommendation'),
        ('improvement', 'Improvement Suggestion'),
        ('weakness', 'Weakness Alert'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    related_module = models.ForeignKey(
        'education.Module', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.recommendation_type} for {self.user.username}"


class UserFeedback(models.Model):
    """User feedback on the platform."""

    FEEDBACK_TYPE_CHOICES = [
        ('general', 'General Feedback'),
        ('module', 'Module Feedback'),
        ('simulation', 'Simulation Feedback'),
        ('bug', 'Bug Report'),
        ('suggestion', 'Suggestion'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    related_module = models.ForeignKey(
        'education.Module', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    related_simulation = models.ForeignKey(
        'simulations.Simulation', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_resolved = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.feedback_type}: {self.subject}"
