import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from education.models import Category, Video
from .models import (
    AdaptiveQuestion, AdaptiveQuizAttempt, AdaptiveQuizAnswer,
    UserKnowledgeProfile
)
from ml_engine.services.knowledge_analyzer import KnowledgeAnalyzer
from ml_engine.services.badge_service import check_and_award_badges


@login_required
def category_list(request):
    """List all quiz categories with user's proficiency per category."""
    categories = Category.objects.all()

    # Attach user's knowledge profile to each category
    profiles = {
        p.category_id: p
        for p in UserKnowledgeProfile.objects.filter(user=request.user).select_related('category')
    }

    category_data = []
    for cat in categories:
        profile = profiles.get(cat.id)
        category_data.append({
            'category': cat,
            'profile': profile,
            'question_count': cat.adaptive_questions.filter(is_active=True).count(),
            'attempt_count': AdaptiveQuizAttempt.objects.filter(
                user=request.user, category=cat, status='completed'
            ).count(),
        })

    return render(request, 'quiz/category_list.html', {
        'category_data': category_data,
    })


@login_required
def category_detail(request, slug):
    """Single category page with quiz start options and videos."""
    category = get_object_or_404(Category, slug=slug)
    profile = UserKnowledgeProfile.objects.filter(user=request.user, category=category).first()
    recent_attempts = AdaptiveQuizAttempt.objects.filter(
        user=request.user, category=category, status='completed'
    ).order_by('-completed_at')[:5]
    videos = category.videos.filter(status='published')

    return render(request, 'quiz/category_detail.html', {
        'category': category,
        'profile': profile,
        'recent_attempts': recent_attempts,
        'videos': videos,
        'question_count': category.adaptive_questions.filter(is_active=True).count(),
    })


@login_required
def start_quiz(request, slug):
    """Start a new quiz attempt for the given category."""
    category = get_object_or_404(Category, slug=slug)
    quiz_type = request.GET.get('type', 'adaptive')
    num_questions = int(request.GET.get('num', 10))

    # Get all active questions for this category
    all_questions = list(
        AdaptiveQuestion.objects.filter(category=category, is_active=True)
    )

    if not all_questions:
        return redirect('quiz:category_detail', slug=slug)

    # Get user's knowledge profile
    profile = UserKnowledgeProfile.objects.filter(user=request.user, category=category).first()

    # Select questions based on quiz type
    if quiz_type == 'pre_test':
        questions = _select_pretest_questions(all_questions, num_questions)
    elif quiz_type == 'adaptive':
        questions = _select_adaptive_questions(all_questions, num_questions, profile)
    else:
        random.shuffle(all_questions)
        questions = all_questions[:num_questions]

    if not questions:
        return redirect('quiz:category_detail', slug=slug)

    # Create the attempt
    attempt = AdaptiveQuizAttempt.objects.create(
        user=request.user,
        category=category,
        quiz_type=quiz_type,
        total_questions=len(questions),
        status='in_progress',
    )

    # Prepare question data for the template (embedded as JSON)
    questions_json = json.dumps([
        {
            'id': q.id,
            'question': q.question,
            'scenario': q.scenario or '',
            'options': q.options,
            'difficulty': q.difficulty,
            'order': i + 1,
        }
        for i, q in enumerate(questions)
    ])

    return render(request, 'quiz/quiz_session.html', {
        'attempt': attempt,
        'category': category,
        'questions_json': questions_json,
        'total_questions': len(questions),
        'quiz_type': quiz_type,
    })


@login_required
@require_POST
def api_submit_answer(request):
    """AJAX endpoint: submit a single answer."""
    try:
        data = json.loads(request.body)
        attempt_id = data.get('attempt_id')
        question_id = data.get('question_id')
        selected = data.get('selected_answer')
        time_seconds = data.get('time_seconds')
        order = data.get('question_order', 0)

        attempt = get_object_or_404(AdaptiveQuizAttempt, id=attempt_id, user=request.user)
        question = get_object_or_404(AdaptiveQuestion, id=question_id)

        is_correct = (selected == question.correct_answer)

        AdaptiveQuizAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={
                'selected_answer': selected,
                'is_correct': is_correct,
                'time_taken_seconds': time_seconds,
                'question_order': order,
            }
        )

        return JsonResponse({
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_POST
def api_complete_quiz(request):
    """AJAX endpoint: finalise quiz attempt and run knowledge estimation."""
    try:
        data = json.loads(request.body)
        attempt_id = data.get('attempt_id')
        time_seconds = data.get('time_seconds')

        attempt = get_object_or_404(AdaptiveQuizAttempt, id=attempt_id, user=request.user)

        if attempt.status != 'in_progress':
            return JsonResponse({'error': 'Attempt already completed'}, status=400)

        answers = AdaptiveQuizAnswer.objects.filter(attempt=attempt).select_related('question')
        correct_count = answers.filter(is_correct=True).count()
        total = attempt.total_questions or answers.count()

        score_pct = (correct_count / total * 100) if total > 0 else 0

        # Build answer list for ML knowledge estimation
        answer_list = [
            {
                'category_id': attempt.category_id,
                'difficulty': a.question.difficulty,
                'is_correct': a.is_correct,
                'time_seconds': a.time_taken_seconds,
            }
            for a in answers
        ]

        # Get current profile
        current_profile = UserKnowledgeProfile.objects.filter(
            user=request.user, category=attempt.category
        ).first()
        current_profiles = []
        if current_profile:
            current_profiles = [{
                'category_id': current_profile.category_id,
                'proficiency_score': current_profile.proficiency_score,
                'estimated_level': current_profile.estimated_level,
            }]

        # Run Bayesian knowledge estimation
        analyzer = KnowledgeAnalyzer()
        result = analyzer.assess_knowledge(answer_list, current_profiles)

        # Update knowledge profile
        for updated in result.get('updated_profiles', []):
            if updated['category_id'] == attempt.category_id:
                UserKnowledgeProfile.objects.update_or_create(
                    user=request.user,
                    category=attempt.category,
                    defaults={
                        'estimated_level': updated['estimated_level'],
                        'proficiency_score': updated['proficiency_score'],
                        'confidence': updated['confidence'],
                        'total_questions_answered': (
                            (current_profile.total_questions_answered if current_profile else 0) + total
                        ),
                        'correct_answers_count': (
                            (current_profile.correct_answers_count if current_profile else 0) + correct_count
                        ),
                        'last_assessed_at': timezone.now(),
                    }
                )
                estimated_level = updated['estimated_level']
                break
        else:
            estimated_level = result.get('overall_level', 'beginner')

        # Save attempt results
        difficulty_progression = [a.question.difficulty for a in answers]
        attempt.correct_answers = correct_count
        attempt.score_percentage = round(score_pct, 2)
        attempt.estimated_level = estimated_level
        attempt.time_taken_seconds = time_seconds
        attempt.difficulty_progression = difficulty_progression
        attempt.status = 'completed'
        attempt.completed_at = timezone.now()
        attempt.save()

        # Check for new badges
        new_badges = check_and_award_badges(request.user)

        return JsonResponse({
            'score_percentage': round(score_pct, 2),
            'correct_answers': correct_count,
            'total_questions': total,
            'estimated_level': estimated_level,
            'new_badges': [{'name': b.name, 'icon': b.icon, 'description': b.description} for b in new_badges],
            'attempt_id': attempt.id,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def quiz_result(request, attempt_id):
    """Show quiz results with answer review."""
    attempt = get_object_or_404(AdaptiveQuizAttempt, id=attempt_id, user=request.user)
    answers = AdaptiveQuizAnswer.objects.filter(attempt=attempt).select_related('question').order_by('question_order')

    profile = None
    if attempt.category:
        profile = UserKnowledgeProfile.objects.filter(
            user=request.user, category=attempt.category
        ).first()

    from badges.models import UserBadge
    recent_badges = UserBadge.objects.filter(user=request.user).select_related('badge').order_by('-earned_at')[:5]

    return render(request, 'quiz/quiz_result.html', {
        'attempt': attempt,
        'answers': answers,
        'profile': profile,
        'recent_badges': recent_badges,
    })


@login_required
def quiz_history(request):
    """Show all quiz attempts for the current user."""
    attempts = AdaptiveQuizAttempt.objects.filter(
        user=request.user
    ).select_related('category').order_by('-started_at')

    return render(request, 'quiz/quiz_history.html', {'attempts': attempts})


@login_required
def knowledge_profile(request):
    """Show user's knowledge profile across all categories."""
    profiles = UserKnowledgeProfile.objects.filter(
        user=request.user
    ).select_related('category').order_by('category__sort_order')

    from badges.models import Badge, UserBadge
    earned_ids = set(UserBadge.objects.filter(user=request.user).values_list('badge_id', flat=True))
    all_badges = Badge.objects.all()
    badges_data = [
        {'badge': b, 'earned': b.id in earned_ids}
        for b in all_badges
    ]

    return render(request, 'quiz/knowledge_profile.html', {
        'profiles': profiles,
        'badges_data': badges_data,
    })


@login_required
def videos_list(request):
    """List all educational videos grouped by category."""
    from accounts.models import ContentProgress
    categories = Category.objects.prefetch_related('videos').all()
    watched_ids = set(
        ContentProgress.objects.filter(
            user=request.user, trackable_type='video', completed=True
        ).values_list('trackable_id', flat=True)
    )

    return render(request, 'quiz/videos_list.html', {
        'categories': categories,
        'watched_ids': watched_ids,
    })


@login_required
@require_POST
def mark_video_watched(request, video_id):
    """Mark a video as watched."""
    from accounts.models import ContentProgress
    ContentProgress.objects.update_or_create(
        user=request.user,
        trackable_type='video',
        trackable_id=video_id,
        defaults={'completed': True, 'completed_at': timezone.now()},
    )
    check_and_award_badges(request.user)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def chatbot_message(request):
    """Chatbot AJAX endpoint."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()[:500]
        history = data.get('history', [])[:10]

        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        from ml_engine.models.chatbot import chatbot
        result = chatbot.get_response(message, history)

        return JsonResponse({
            'reply': result['reply'],
            'confidence': result['confidence'],
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _select_pretest_questions(questions, num):
    by_diff = {'beginner': [], 'intermediate': [], 'advanced': []}
    for q in questions:
        by_diff.get(q.difficulty, by_diff['beginner']).append(q)

    selected = []
    per_level = max(1, num // 3)
    for diff in ['beginner', 'intermediate', 'advanced']:
        pool = by_diff[diff][:]
        random.shuffle(pool)
        selected.extend(pool[:per_level])

    remaining = [q for q in questions if q not in selected]
    random.shuffle(remaining)
    while len(selected) < num and remaining:
        selected.append(remaining.pop())

    return selected[:num]


def _select_adaptive_questions(questions, num, profile):
    if profile:
        score = profile.proficiency_score
    else:
        score = 0.3

    if score < 0.35:
        target = 'beginner'
    elif score < 0.70:
        target = 'intermediate'
    else:
        target = 'advanced'

    diff_order = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
    target_idx = diff_order[target]

    questions_sorted = sorted(
        questions,
        key=lambda q: (abs(diff_order.get(q.difficulty, 0) - target_idx), random.random())
    )
    selected = questions_sorted[:num]
    selected.sort(key=lambda q: diff_order.get(q.difficulty, 0))
    return selected
