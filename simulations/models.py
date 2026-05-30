from django.db import models
from django.conf import settings
import uuid


class PhishingTemplate(models.Model):
    """Template for phishing simulation emails/SMS."""

    TEMPLATE_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    SCENARIO_CHOICES = [
        ('banking', 'Banking/Financial'),
        ('social_media', 'Social Media'),
        ('ecommerce', 'E-commerce'),
        ('government', 'Government'),
        ('corporate', 'Corporate'),
        ('prize', 'Prize/Lottery'),
        ('technical', 'Technical Support'),
        ('delivery', 'Delivery/Shipping'),
    ]

    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=10, choices=TEMPLATE_TYPE_CHOICES)
    scenario = models.CharField(max_length=20, choices=SCENARIO_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')

    # Email fields
    sender_name = models.CharField(max_length=100, blank=True)
    sender_email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, blank=True)

    # Content
    content = models.TextField()
    html_content = models.TextField(blank=True)

    # SMS fields
    sender_number = models.CharField(max_length=20, blank=True)

    # Phishing indicators in this template
    indicators = models.ManyToManyField('education.PhishingIndicator', blank=True)

    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.template_type})"


class Simulation(models.Model):
    """A simulation instance for a user."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='simulations')
    template = models.ForeignKey(PhishingTemplate, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # User's response
    user_clicked_link = models.BooleanField(default=False)
    user_submitted_data = models.BooleanField(default=False)
    user_reported = models.BooleanField(default=False)
    user_identified_correctly = models.BooleanField(null=True)

    # Indicators identified by user
    indicators_identified = models.ManyToManyField('education.PhishingIndicator', blank=True)

    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_seconds = models.IntegerField(null=True, blank=True)

    # Scoring
    score = models.FloatField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)

    # Feedback
    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Simulation {self.id} - {self.user.username}"

    def calculate_score(self):
        """Calculate simulation score based on user actions."""
        score = 0

        # Did not click malicious link
        if not self.user_clicked_link:
            score += 30

        # Did not submit data
        if not self.user_submitted_data:
            score += 30

        # Reported the phishing attempt
        if self.user_reported:
            score += 20

        # Correctly identified as phishing
        if self.user_identified_correctly:
            score += 20

        # Bonus for identifying indicators
        total_indicators = self.template.indicators.count()
        if total_indicators > 0:
            identified = self.indicators_identified.count()
            indicator_score = (identified / total_indicators) * 20
            score += indicator_score

        self.score = min(score, 100)
        return self.score


class SimulationFeedback(models.Model):
    """Detailed feedback for a simulation."""

    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE, related_name='detailed_feedback')
    correct_indicators = models.ManyToManyField('education.PhishingIndicator', related_name='correct_in_simulations')
    missed_indicators = models.ManyToManyField('education.PhishingIndicator', related_name='missed_in_simulations')
    explanation = models.TextField()
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f"Feedback for {self.simulation.id}"


class SimulationCampaign(models.Model):
    """Group simulations into campaigns for tracking."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    templates = models.ManyToManyField(PhishingTemplate)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
