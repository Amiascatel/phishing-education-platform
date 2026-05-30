from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
import random

from .models import Quiz, Question, Answer, QuizAttempt, QuizResponse, AssessmentResult
from analytics.models import UserActivity


@login_required
def quiz_list(request):
    """List available quizzes."""
    quizzes = Quiz.objects.filter(is_active=True)

    # Get user's attempt counts
    user_attempts = {}
    for quiz in quizzes:
        attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
        user_attempts[quiz.id] = attempts

    context = {
        'quizzes': quizzes,
        'user_attempts': user_attempts,
    }
    return render(request, 'assessments/quiz_list.html', context)


@login_required
def pre_assessment(request):
    """Start or continue pre-assessment."""
    user = request.user

    if user.pre_assessment_completed:
        messages.info(request, 'You have already completed the pre-assessment.')
        return redirect('assessments:assessment_results')

    quiz = Quiz.objects.filter(quiz_type='pre_assessment', is_active=True).first()
    if not quiz:
        messages.error(request, 'Pre-assessment quiz is not available.')
        return redirect('education:dashboard')

    return redirect('assessments:take_quiz', quiz_id=quiz.id)


@login_required
def post_assessment(request):
    """Start or continue post-assessment."""
    user = request.user

    if not user.pre_assessment_completed:
        messages.warning(request, 'Please complete the pre-assessment first.')
        return redirect('assessments:pre_assessment')

    if user.post_assessment_completed:
        messages.info(request, 'You have already completed the post-assessment.')
        return redirect('assessments:assessment_results')

    quiz = Quiz.objects.filter(quiz_type='post_assessment', is_active=True).first()
    if not quiz:
        messages.error(request, 'Post-assessment quiz is not available.')
        return redirect('education:dashboard')

    return redirect('assessments:take_quiz', quiz_id=quiz.id)


@login_required
def take_quiz(request, quiz_id):
    """Take a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Create new attempt
    attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)

    # Log activity
    UserActivity.objects.create(
        user=request.user,
        activity_type='quiz_start',
        description=f'Started quiz: {quiz.title}',
        metadata={'quiz_id': quiz.id, 'attempt_id': attempt.id}
    )

    # Get questions
    questions = list(quiz.questions.all())
    if quiz.shuffle_questions:
        random.shuffle(questions)

    # Store question order in session
    request.session[f'quiz_{attempt.id}_questions'] = [q.id for q in questions]
    request.session[f'quiz_{attempt.id}_current'] = 0

    return redirect('assessments:quiz_question', attempt_id=attempt.id)


@login_required
def quiz_question(request, attempt_id):
    """Display current quiz question."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

    if attempt.completed_at:
        return redirect('assessments:quiz_result', attempt_id=attempt_id)

    question_ids = request.session.get(f'quiz_{attempt_id}_questions', [])
    current_index = request.session.get(f'quiz_{attempt_id}_current', 0)

    if current_index >= len(question_ids):
        return redirect('assessments:complete_quiz', attempt_id=attempt_id)

    question = get_object_or_404(Question, id=question_ids[current_index])
    answers = list(question.answers.all())
    random.shuffle(answers)

    # Check if already answered
    existing_response = QuizResponse.objects.filter(attempt=attempt, question=question).first()

    context = {
        'attempt': attempt,
        'question': question,
        'answers': answers,
        'current': current_index + 1,
        'total': len(question_ids),
        'existing_response': existing_response,
        'time_limit': attempt.quiz.time_limit_minutes,
    }
    return render(request, 'assessments/quiz_question.html', context)


@login_required
@require_POST
def submit_answer(request, attempt_id):
    """Submit answer for a question."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

    if attempt.completed_at:
        return JsonResponse({'error': 'Quiz already completed'}, status=400)

    data = json.loads(request.body)
    question_id = data.get('question_id')
    answer_id = data.get('answer_id')
    text_response = data.get('text_response', '')

    question = get_object_or_404(Question, id=question_id)

    # Create or update response
    response, created = QuizResponse.objects.get_or_create(
        attempt=attempt,
        question=question,
        defaults={'text_response': text_response}
    )

    if answer_id:
        answer = get_object_or_404(Answer, id=answer_id)
        response.selected_answer = answer
    response.text_response = text_response
    response.save()

    # Check answer
    response.check_answer()

    # Move to next question
    current_index = request.session.get(f'quiz_{attempt_id}_current', 0)
    request.session[f'quiz_{attempt_id}_current'] = current_index + 1

    question_ids = request.session.get(f'quiz_{attempt_id}_questions', [])

    if current_index + 1 >= len(question_ids):
        return JsonResponse({
            'success': True,
            'next_url': f'/assessments/quiz/{attempt_id}/complete/'
        })

    return JsonResponse({
        'success': True,
        'next_url': f'/assessments/quiz/{attempt_id}/question/'
    })


@login_required
def complete_quiz(request, attempt_id):
    """Complete the quiz and calculate score."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

    if not attempt.completed_at:
        attempt.completed_at = timezone.now()
        time_diff = attempt.completed_at - attempt.started_at
        attempt.time_taken_seconds = int(time_diff.total_seconds())

        # Calculate score
        attempt.calculate_score()
        attempt.save()

        # Update user assessment status
        user = request.user
        quiz = attempt.quiz

        if quiz.quiz_type == 'pre_assessment':
            user.pre_assessment_completed = True
            user.pre_assessment_score = attempt.percentage
            user.save()

            # Create assessment result
            AssessmentResult.objects.create(
                user=user,
                assessment_type='pre_assessment',
                quiz_attempt=attempt
            )

        elif quiz.quiz_type == 'post_assessment':
            user.post_assessment_completed = True
            user.post_assessment_score = attempt.percentage
            user.save()

            # Create assessment result
            AssessmentResult.objects.create(
                user=user,
                assessment_type='post_assessment',
                quiz_attempt=attempt
            )

        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='quiz_complete',
            description=f'Completed quiz: {quiz.title} with score: {attempt.percentage}%',
            metadata={
                'quiz_id': quiz.id,
                'attempt_id': attempt.id,
                'score': attempt.percentage,
                'passed': attempt.passed
            }
        )

    return redirect('assessments:quiz_result', attempt_id=attempt_id)


@login_required
def quiz_result(request, attempt_id):
    """View quiz results."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    responses = attempt.responses.select_related('question', 'selected_answer').all()

    context = {
        'attempt': attempt,
        'responses': responses,
        'show_answers': attempt.quiz.show_correct_answers,
    }
    return render(request, 'assessments/quiz_result.html', context)


@login_required
def assessment_results(request):
    """View pre/post assessment comparison."""
    user = request.user

    pre_result = AssessmentResult.objects.filter(
        user=user, assessment_type='pre_assessment'
    ).first()

    post_result = AssessmentResult.objects.filter(
        user=user, assessment_type='post_assessment'
    ).first()

    improvement = None
    if pre_result and post_result:
        improvement = post_result.quiz_attempt.percentage - pre_result.quiz_attempt.percentage

    context = {
        'pre_result': pre_result,
        'post_result': post_result,
        'improvement': improvement,
    }
    return render(request, 'assessments/assessment_results.html', context)


@login_required
def quiz_history(request):
    """View user's quiz history."""
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz')

    context = {
        'attempts': attempts,
    }
    return render(request, 'assessments/quiz_history.html', context)
