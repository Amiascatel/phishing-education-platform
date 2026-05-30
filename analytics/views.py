from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta

from .models import (
    UserActivity, LearningAnalytics, PerformanceSnapshot,
    AIRecommendation, UserFeedback
)
from accounts.models import User, UserProgress
from simulations.models import Simulation
from assessments.models import QuizAttempt
from education.models import Module


@login_required
def analytics_dashboard(request):
    """User analytics dashboard."""
    user = request.user

    # Get or create learning analytics
    analytics, _ = LearningAnalytics.objects.get_or_create(user=user)

    # Get recent activities
    recent_activities = UserActivity.objects.filter(user=user)[:10]

    # Get performance snapshots for chart
    snapshots = PerformanceSnapshot.objects.filter(user=user).order_by('date')[:30]

    # Calculate statistics
    total_simulations = Simulation.objects.filter(user=user, status='completed').count()
    total_quizzes = QuizAttempt.objects.filter(user=user, completed_at__isnull=False).count()
    total_modules = UserProgress.objects.filter(user=user, completed=True).count()

    # Average scores
    avg_simulation_score = Simulation.objects.filter(
        user=user, status='completed'
    ).aggregate(avg=Avg('score'))['avg'] or 0

    avg_quiz_score = QuizAttempt.objects.filter(
        user=user, completed_at__isnull=False
    ).aggregate(avg=Avg('percentage'))['avg'] or 0

    # Get AI recommendations
    recommendations = AIRecommendation.objects.filter(
        user=user, is_dismissed=False
    ).order_by('-priority')[:5]

    context = {
        'analytics': analytics,
        'recent_activities': recent_activities,
        'snapshots': snapshots,
        'total_simulations': total_simulations,
        'total_quizzes': total_quizzes,
        'total_modules': total_modules,
        'avg_simulation_score': round(avg_simulation_score, 1),
        'avg_quiz_score': round(avg_quiz_score, 1),
        'recommendations': recommendations,
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def performance_chart_data(request):
    """Get performance data for charts."""
    user = request.user

    # Get last 30 days of data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    snapshots = PerformanceSnapshot.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')

    data = {
        'labels': [s.date.strftime('%Y-%m-%d') for s in snapshots],
        'overall': [s.overall_score for s in snapshots],
        'email': [s.email_phishing_score for s in snapshots],
        'sms': [s.sms_phishing_score for s in snapshots],
        'social': [s.social_engineering_score for s in snapshots],
    }

    return JsonResponse(data)


@login_required
def activity_feed(request):
    """View all user activities."""
    activities = UserActivity.objects.filter(user=request.user)

    # Filter by type
    activity_type = request.GET.get('type')
    if activity_type:
        activities = activities.filter(activity_type=activity_type)

    context = {
        'activities': activities,
        'activity_types': UserActivity.ACTIVITY_TYPE_CHOICES,
    }
    return render(request, 'analytics/activity_feed.html', context)


@login_required
def dismiss_recommendation(request, recommendation_id):
    """Dismiss an AI recommendation."""
    recommendation = AIRecommendation.objects.filter(
        id=recommendation_id, user=request.user
    ).first()

    if recommendation:
        recommendation.is_dismissed = True
        recommendation.save()
        messages.success(request, 'Recommendation dismissed.')

    return redirect('analytics:dashboard')


@login_required
def submit_feedback(request):
    """Submit user feedback."""
    if request.method == 'POST':
        feedback_type = request.POST.get('feedback_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        UserFeedback.objects.create(
            user=request.user,
            feedback_type=feedback_type,
            subject=subject,
            message=message,
            rating=int(rating) if rating else None
        )

        messages.success(request, 'Thank you for your feedback!')
        return redirect('analytics:dashboard')

    context = {
        'feedback_types': UserFeedback.FEEDBACK_TYPE_CHOICES,
    }
    return render(request, 'analytics/submit_feedback.html', context)


@login_required
def leaderboard(request):
    """View platform leaderboard."""
    # Top users by points
    top_by_points = User.objects.order_by('-total_points')[:20]

    # Top users by completed modules
    top_by_modules = User.objects.order_by('-completed_modules')[:20]

    # Top users by simulation scores
    top_by_simulations = User.objects.filter(
        email_phishing_score__gt=0
    ).order_by('-email_phishing_score')[:20]

    # User's rank
    user_rank = User.objects.filter(total_points__gt=request.user.total_points).count() + 1

    context = {
        'top_by_points': top_by_points,
        'top_by_modules': top_by_modules,
        'top_by_simulations': top_by_simulations,
        'user_rank': user_rank,
    }
    return render(request, 'analytics/leaderboard.html', context)


@login_required
def skill_breakdown(request):
    """Detailed breakdown of user's skills."""
    user = request.user

    # Get simulation performance by scenario
    simulation_stats = Simulation.objects.filter(
        user=user, status='completed'
    ).values('template__scenario').annotate(
        count=Count('id'),
        avg_score=Avg('score')
    )

    # Get quiz performance by module type
    quiz_stats = QuizAttempt.objects.filter(
        user=user, completed_at__isnull=False
    ).select_related('quiz__module').values(
        'quiz__module__module_type'
    ).annotate(
        count=Count('id'),
        avg_score=Avg('percentage')
    )

    context = {
        'user': user,
        'simulation_stats': simulation_stats,
        'quiz_stats': quiz_stats,
    }
    return render(request, 'analytics/skill_breakdown.html', context)


def generate_ai_recommendations(user):
    """Generate AI-powered recommendations for a user."""
    recommendations = []

    # Check for weak areas
    if user.email_phishing_score < 50:
        modules = Module.objects.filter(module_type='email_phishing', is_active=True)
        incomplete = modules.exclude(
            id__in=UserProgress.objects.filter(user=user, completed=True).values_list('module_id', flat=True)
        ).first()

        if incomplete:
            recommendations.append({
                'type': 'weakness',
                'title': 'Improve Email Phishing Detection',
                'description': 'Your email phishing detection score is below average.',
                'module': incomplete,
                'priority': 3
            })

    if user.sms_phishing_score < 50:
        modules = Module.objects.filter(module_type='sms_phishing', is_active=True)
        incomplete = modules.exclude(
            id__in=UserProgress.objects.filter(user=user, completed=True).values_list('module_id', flat=True)
        ).first()

        if incomplete:
            recommendations.append({
                'type': 'weakness',
                'title': 'Practice SMS Phishing Detection',
                'description': 'Your SMS phishing detection score needs improvement.',
                'module': incomplete,
                'priority': 3
            })

    # Recommend next module based on progress
    completed_module_ids = UserProgress.objects.filter(
        user=user, completed=True
    ).values_list('module_id', flat=True)

    next_module = Module.objects.filter(
        is_active=True
    ).exclude(id__in=completed_module_ids).order_by('order').first()

    if next_module:
        recommendations.append({
            'type': 'module',
            'title': f'Continue Learning: {next_module.title}',
            'description': f'Ready for the next challenge? Complete the {next_module.title} module.',
            'module': next_module,
            'priority': 2
        })

    # Save recommendations
    for rec in recommendations:
        AIRecommendation.objects.get_or_create(
            user=user,
            recommendation_type=rec['type'],
            title=rec['title'],
            defaults={
                'description': rec['description'],
                'related_module': rec.get('module'),
                'priority': rec['priority']
            }
        )

    return recommendations
