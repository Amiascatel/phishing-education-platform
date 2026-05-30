from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for the phishing education platform."""

    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='beginner')
    total_points = models.IntegerField(default=0)
    completed_modules = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Adaptive learning fields
    email_phishing_score = models.FloatField(default=0.0)
    sms_phishing_score = models.FloatField(default=0.0)
    social_engineering_score = models.FloatField(default=0.0)

    # Pre/Post assessment tracking
    pre_assessment_completed = models.BooleanField(default=False)
    pre_assessment_score = models.FloatField(null=True, blank=True)
    post_assessment_completed = models.BooleanField(default=False)
    post_assessment_score = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_overall_score(self):
        """Calculate overall phishing detection score."""
        scores = [self.email_phishing_score, self.sms_phishing_score, self.social_engineering_score]
        return sum(scores) / len(scores) if scores else 0.0

    def update_skill_level(self):
        """Update skill level based on overall score."""
        overall = self.get_overall_score()
        if overall >= 80:
            self.skill_level = 'advanced'
        elif overall >= 50:
            self.skill_level = 'intermediate'
        else:
            self.skill_level = 'beginner'
        self.save()


class UserProgress(models.Model):
    """Track user's learning progress."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    module = models.ForeignKey('education.Module', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    attempts = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'module']
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress Records'

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"


class LearningPath(models.Model):
    """Personalized learning path for users based on AI recommendations."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    recommended_modules = models.ManyToManyField('education.Module', blank=True)
    focus_area = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Learning Path for {self.user.username}"


class ContentProgress(models.Model):
    """Tracks completion of individual lessons and videos."""

    TRACKABLE_CHOICES = [
        ('lesson', 'Lesson'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_progress')
    trackable_type = models.CharField(max_length=20, choices=TRACKABLE_CHOICES)
    trackable_id = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_seconds = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'trackable_type', 'trackable_id']
        indexes = [
            models.Index(fields=['user', 'trackable_type']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.trackable_type}:{self.trackable_id}"
