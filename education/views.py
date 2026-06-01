from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Count

from .models import Category, Module, Lesson, PhishingIndicator, Resource
from accounts.models import UserProgress
from analytics.models import UserActivity, AIRecommendation


@login_required
def dashboard(request):
    """Main dashboard view."""
    user = request.user

    # Get user progress
    completed_modules = UserProgress.objects.filter(user=user, completed=True).count()
    in_progress_modules = UserProgress.objects.filter(user=user, completed=False).count()

    # Get recent modules
    recent_progress = UserProgress.objects.filter(user=user).order_by('-completion_date')[:5]

    # Get recommended modules
    recommendations = AIRecommendation.objects.filter(
        user=user,
        is_dismissed=False,
        recommendation_type='module'
    )[:3]

    # Get all categories with module counts
    categories = Category.objects.annotate(module_count=Count('modules'))

    # Calculate overall progress
    total_modules = Module.objects.filter(is_active=True).count()
    progress_percentage = (completed_modules / total_modules * 100) if total_modules > 0 else 0

    context = {
        'user': user,
        'completed_modules': completed_modules,
        'in_progress_modules': in_progress_modules,
        'recent_progress': recent_progress,
        'recommendations': recommendations,
        'categories': categories,
        'progress_percentage': progress_percentage,
        'total_modules': total_modules,
    }
    return render(request, 'education/dashboard.html', context)


@login_required
def module_list(request):
    """List all available modules."""
    module_type = request.GET.get('type', '')
    difficulty  = request.GET.get('difficulty', '')

    # Cache shared catalogue data (same for all users, only changes when admin edits)
    cat_key = f'edu:module_list:{module_type}:{difficulty}'
    cached  = cache.get(cat_key)
    if cached:
        categories, modules = cached
    else:
        categories = list(Category.objects.prefetch_related('modules').all())
        modules_qs = Module.objects.filter(is_active=True).select_related('category')
        if module_type:
            modules_qs = modules_qs.filter(module_type=module_type)
        if difficulty:
            modules_qs = modules_qs.filter(difficulty=difficulty)
        modules = list(modules_qs)
        cache.set(cat_key, (categories, modules), 60 * 10)  # 10 minutes

    # User progress is personal — never cache
    user_progress = {
        p.module_id: p for p in UserProgress.objects.filter(user=request.user)
    }

    return render(request, 'education/module_list.html', {
        'categories': categories,
        'modules': modules,
        'user_progress': user_progress,
        'module_types': Module.MODULE_TYPE_CHOICES,
        'difficulty_levels': Module.DIFFICULTY_CHOICES,
    })


@login_required
def module_detail(request, slug):
    """View module details and content."""
    module = get_object_or_404(Module, slug=slug, is_active=True)
    lessons = module.lessons.all()
    resources = module.resources.all()

    # Get or create user progress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        module=module,
        defaults={'attempts': 0}
    )

    if created:
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='module_start',
            description=f'Started module: {module.title}',
            metadata={'module_id': module.id}
        )

    context = {
        'module': module,
        'lessons': lessons,
        'resources': resources,
        'progress': progress,
    }
    return render(request, 'education/module_detail.html', context)


@login_required
def lesson_view(request, slug, lesson_id):
    """View a specific lesson."""
    module = get_object_or_404(Module, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)

    # Get next and previous lessons
    lessons = list(module.lessons.all())
    current_index = next((i for i, l in enumerate(lessons) if l.id == lesson.id), 0)

    prev_lesson = lessons[current_index - 1] if current_index > 0 else None
    next_lesson = lessons[current_index + 1] if current_index < len(lessons) - 1 else None

    context = {
        'module': module,
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'total_lessons': len(lessons),
        'current_lesson': current_index + 1,
    }
    return render(request, 'education/lesson.html', context)


@login_required
def complete_module(request, slug):
    """Mark a module as complete."""
    module = get_object_or_404(Module, slug=slug)
    progress, _ = UserProgress.objects.get_or_create(user=request.user, module=module)

    if not progress.completed:
        progress.completed = True
        progress.completion_date = timezone.now()
        progress.save()

        # Update user stats
        request.user.completed_modules += 1
        request.user.total_points += module.points
        request.user.save()

        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='module_complete',
            description=f'Completed module: {module.title}',
            metadata={'module_id': module.id, 'points': module.points}
        )

        messages.success(request, f'Congratulations! You completed "{module.title}" and earned {module.points} points!')

    return redirect('education:module_detail', slug=slug)


@login_required
def phishing_indicators(request):
    """View all phishing indicators."""
    indicators = PhishingIndicator.objects.all().order_by('indicator_type', 'name')

    # Group by type
    grouped_indicators = {}
    for indicator in indicators:
        if indicator.indicator_type not in grouped_indicators:
            grouped_indicators[indicator.indicator_type] = []
        grouped_indicators[indicator.indicator_type].append(indicator)

    context = {
        'indicators': indicators,
        'grouped_indicators': grouped_indicators,
    }
    return render(request, 'education/phishing_indicators.html', context)


@login_required
def resources_view(request):
    """View all learning resources."""
    resources = Resource.objects.all().order_by('-created_at')

    # Filter by type
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)

    context = {
        'resources': resources,
        'resource_types': Resource.RESOURCE_TYPE_CHOICES,
    }
    return render(request, 'education/resources.html', context)
