from django.db import models
from django.conf import settings


class Badge(models.Model):
    """Achievement badge that users can earn."""

    CATEGORY_CHOICES = [
        ('learning', 'Learning'),
        ('quiz', 'Quiz'),
        ('engagement', 'Engagement'),
        ('mastery', 'Mastery'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    requirement = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='quiz')
    # JSON dict defining award criteria
    # e.g. {"type": "quiz_score", "category_slug": "email-phishing", "min_score": 80}
    criteria = models.JSONField(default=dict)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Badge earned by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='earned_badges'
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"
