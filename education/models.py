from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """Category for educational modules and quiz topics."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='BookOpenIcon')
    color = models.CharField(max_length=30, default='blue')
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Module(models.Model):
    """Educational module for phishing awareness."""

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    MODULE_TYPE_CHOICES = [
        ('email_phishing', 'Email Phishing'),
        ('sms_phishing', 'SMS Phishing (Smishing)'),
        ('social_engineering', 'Social Engineering'),
        ('general', 'General Awareness'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='modules')
    module_type = models.CharField(max_length=30, choices=MODULE_TYPE_CHOICES, default='general')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    duration_minutes = models.IntegerField(default=10)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Prerequisites
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Individual lesson within a module."""

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)
    has_interactive = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class PhishingIndicator(models.Model):
    """Common phishing indicators for education."""

    INDICATOR_TYPE_CHOICES = [
        ('url', 'URL Indicator'),
        ('sender', 'Sender Indicator'),
        ('content', 'Content Indicator'),
        ('attachment', 'Attachment Indicator'),
        ('urgency', 'Urgency Indicator'),
    ]

    name = models.CharField(max_length=100)
    indicator_type = models.CharField(max_length=20, choices=INDICATOR_TYPE_CHOICES)
    description = models.TextField()
    example = models.TextField()
    severity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.indicator_type})"


class Resource(models.Model):
    """Additional learning resources."""

    RESOURCE_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('infographic', 'Infographic'),
        ('document', 'Document'),
        ('external', 'External Link'),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    """Educational video linked to a quiz/education category."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    url = models.URLField()
    duration = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title
