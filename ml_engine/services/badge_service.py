"""
Badge Service

Checks badge criteria and awards badges to users after quiz completion
or lesson/video progress updates.
"""

from django.utils import timezone


def check_and_award_badges(user) -> list:
    """
    Check all badge criteria and award any newly earned badges.
    Returns list of newly awarded Badge objects.
    """
    from badges.models import Badge, UserBadge

    awarded = []
    existing_ids = set(
        UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    )

    for badge in Badge.objects.all():
        if badge.id in existing_ids:
            continue
        if _meets_criteria(user, badge):
            UserBadge.objects.create(user=user, badge=badge)
            awarded.append(badge)

    return awarded


def _meets_criteria(user, badge) -> bool:
    criteria = badge.criteria
    if not criteria or 'type' not in criteria:
        return False

    ctype = criteria['type']
    if ctype == 'lessons_completed':
        return _check_lessons_completed(user, criteria)
    elif ctype == 'quiz_score':
        return _check_quiz_score(user, criteria)
    elif ctype == 'all_quizzes_avg':
        return _check_all_quizzes_avg(user, criteria)
    elif ctype == 'perfect_score':
        return _check_perfect_score(user)
    elif ctype == 'all_videos_watched':
        return _check_all_videos_watched(user)
    elif ctype == 'platform_complete':
        return _check_platform_complete(user)
    elif ctype == 'quiz_attempts':
        return _check_quiz_attempts(user, criteria)
    return False


def _check_lessons_completed(user, criteria) -> bool:
    from accounts.models import ContentProgress
    count = ContentProgress.objects.filter(
        user=user, trackable_type='lesson', completed=True
    ).count()
    return count >= criteria.get('count', 1)


def _check_quiz_score(user, criteria) -> bool:
    from quiz.models import AdaptiveQuizAttempt
    from education.models import Category
    cat_slug = criteria.get('category_slug')
    min_score = criteria.get('min_score', 80)
    qs = AdaptiveQuizAttempt.objects.filter(user=user, status='completed')
    if cat_slug:
        try:
            cat = Category.objects.get(slug=cat_slug)
            qs = qs.filter(category=cat)
        except Category.DoesNotExist:
            return False
    return qs.filter(score_percentage__gte=min_score).exists()


def _check_all_quizzes_avg(user, criteria) -> bool:
    from quiz.models import AdaptiveQuizAttempt
    attempts = AdaptiveQuizAttempt.objects.filter(user=user, status='completed')
    if not attempts.exists():
        return False
    scores = [a.score_percentage for a in attempts if a.score_percentage is not None]
    if not scores:
        return False
    avg = sum(scores) / len(scores)
    return avg >= criteria.get('min_avg', 75)


def _check_perfect_score(user) -> bool:
    from quiz.models import AdaptiveQuizAttempt
    return AdaptiveQuizAttempt.objects.filter(
        user=user, status='completed', score_percentage=100.0
    ).exists()


def _check_all_videos_watched(user) -> bool:
    from accounts.models import ContentProgress
    from education.models import Video
    total = Video.objects.filter(status='published').count()
    if total == 0:
        return False
    watched = ContentProgress.objects.filter(
        user=user, trackable_type='video', completed=True
    ).count()
    return watched >= total


def _check_platform_complete(user) -> bool:
    return _check_lessons_completed(user, {'count': 10}) and _check_all_quizzes_avg(user, {'min_avg': 70})


def _check_quiz_attempts(user, criteria) -> bool:
    from quiz.models import AdaptiveQuizAttempt
    count = AdaptiveQuizAttempt.objects.filter(user=user, status='completed').count()
    return count >= criteria.get('count', 5)
