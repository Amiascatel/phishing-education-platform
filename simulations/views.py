from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

from .models import PhishingTemplate, Simulation, SimulationFeedback
from education.models import PhishingIndicator
from analytics.models import UserActivity


@login_required
def simulation_list(request):
    """List available simulations."""
    templates = PhishingTemplate.objects.filter(is_active=True)

    # Filter by type
    sim_type = request.GET.get('type')
    if sim_type:
        templates = templates.filter(template_type=sim_type)

    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        templates = templates.filter(difficulty=difficulty)

    # Get user's simulation history
    user_simulations = Simulation.objects.filter(user=request.user).values_list('template_id', flat=True)

    context = {
        'templates': templates,
        'user_simulations': list(user_simulations),
        'template_types': PhishingTemplate.TEMPLATE_TYPE_CHOICES,
        'difficulties': PhishingTemplate.DIFFICULTY_CHOICES,
    }
    return render(request, 'simulations/simulation_list.html', context)


@login_required
def start_simulation(request, template_id):
    """Start a new simulation."""
    template = get_object_or_404(PhishingTemplate, id=template_id, is_active=True)

    # Create new simulation
    simulation = Simulation.objects.create(
        user=request.user,
        template=template,
        status='in_progress'
    )

    # Log activity
    UserActivity.objects.create(
        user=request.user,
        activity_type='simulation_start',
        description=f'Started simulation: {template.name}',
        metadata={'simulation_id': str(simulation.id), 'template_type': template.template_type}
    )

    return redirect('simulations:run_simulation', simulation_id=simulation.id)


@login_required
def run_simulation(request, simulation_id):
    """Run the simulation - display phishing content."""
    simulation = get_object_or_404(Simulation, id=simulation_id, user=request.user)

    if simulation.status == 'completed':
        return redirect('simulations:simulation_result', simulation_id=simulation_id)

    template = simulation.template
    indicators = template.indicators.all()

    context = {
        'simulation': simulation,
        'template': template,
        'indicators': indicators,
    }

    if template.template_type == 'email':
        return render(request, 'simulations/email_simulation.html', context)
    else:
        return render(request, 'simulations/sms_simulation.html', context)


@login_required
@require_POST
def submit_simulation(request, simulation_id):
    """Submit simulation response."""
    simulation = get_object_or_404(Simulation, id=simulation_id, user=request.user)

    if simulation.status == 'completed':
        return JsonResponse({'error': 'Simulation already completed'}, status=400)

    data = json.loads(request.body)

    # Update simulation with user response
    simulation.user_clicked_link = data.get('clicked_link', False)
    simulation.user_submitted_data = data.get('submitted_data', False)
    simulation.user_reported = data.get('reported', False)
    simulation.user_identified_correctly = data.get('identified_as_phishing', None)

    # Record identified indicators
    identified_indicator_ids = data.get('indicators', [])
    if identified_indicator_ids:
        indicators = PhishingIndicator.objects.filter(id__in=identified_indicator_ids)
        simulation.indicators_identified.set(indicators)

    # Complete the simulation
    simulation.status = 'completed'
    simulation.completed_at = timezone.now()

    # Calculate time spent
    time_diff = simulation.completed_at - simulation.started_at
    simulation.time_spent_seconds = int(time_diff.total_seconds())

    # Calculate score
    score = simulation.calculate_score()
    simulation.points_earned = int(score / 10)  # Convert to points

    simulation.save()

    # Update user scores based on template type
    user = request.user
    if simulation.template.template_type == 'email':
        # Update email phishing score (weighted average)
        email_sims = Simulation.objects.filter(
            user=user,
            template__template_type='email',
            status='completed'
        )
        avg_score = sum(s.score or 0 for s in email_sims) / email_sims.count() if email_sims.count() > 0 else 0
        user.email_phishing_score = avg_score
    else:
        # Update SMS phishing score
        sms_sims = Simulation.objects.filter(
            user=user,
            template__template_type='sms',
            status='completed'
        )
        avg_score = sum(s.score or 0 for s in sms_sims) / sms_sims.count() if sms_sims.count() > 0 else 0
        user.sms_phishing_score = avg_score

    user.total_points += simulation.points_earned
    user.update_skill_level()

    # Log activity
    UserActivity.objects.create(
        user=request.user,
        activity_type='simulation_complete',
        description=f'Completed simulation with score: {score}',
        metadata={
            'simulation_id': str(simulation.id),
            'score': score,
            'points_earned': simulation.points_earned
        }
    )

    # Create detailed feedback
    template_indicators = set(simulation.template.indicators.all())
    identified = set(simulation.indicators_identified.all())

    correct = template_indicators & identified
    missed = template_indicators - identified

    feedback = SimulationFeedback.objects.create(
        simulation=simulation,
        explanation=generate_feedback_explanation(simulation),
        recommendations=generate_recommendations(simulation, missed)
    )
    feedback.correct_indicators.set(correct)
    feedback.missed_indicators.set(missed)

    return JsonResponse({
        'success': True,
        'score': score,
        'points_earned': simulation.points_earned,
        'redirect_url': f'/simulations/{simulation.id}/result/'
    })


def generate_feedback_explanation(simulation):
    """Generate explanation based on user's actions."""
    explanation = []

    if simulation.user_clicked_link:
        explanation.append("You clicked on a suspicious link. In a real phishing attack, this could lead to malware installation or credential theft.")
    else:
        explanation.append("Good job not clicking on suspicious links!")

    if simulation.user_submitted_data:
        explanation.append("You submitted personal information. Never enter sensitive data on suspicious websites.")
    else:
        explanation.append("You correctly avoided submitting personal information.")

    if simulation.user_reported:
        explanation.append("Excellent! Reporting phishing attempts helps protect others.")

    if simulation.user_identified_correctly:
        explanation.append("You correctly identified this as a phishing attempt!")
    elif simulation.user_identified_correctly is False:
        explanation.append("This was a phishing attempt. Pay attention to the red flags we highlighted.")

    return " ".join(explanation)


def generate_recommendations(simulation, missed_indicators):
    """Generate personalized recommendations."""
    recommendations = []

    if missed_indicators:
        indicator_names = [i.name for i in missed_indicators]
        recommendations.append(f"Focus on learning about these indicators you missed: {', '.join(indicator_names)}")

    if simulation.user_clicked_link:
        recommendations.append("Practice hovering over links to check their true destination before clicking.")

    if simulation.template.template_type == 'email':
        recommendations.append("Always verify the sender's email address carefully.")
    else:
        recommendations.append("Be cautious of unexpected SMS messages asking for personal information.")

    return " ".join(recommendations)


@login_required
def simulation_result(request, simulation_id):
    """View simulation results and feedback."""
    simulation = get_object_or_404(Simulation, id=simulation_id, user=request.user)

    if simulation.status != 'completed':
        return redirect('simulations:run_simulation', simulation_id=simulation_id)

    try:
        feedback = simulation.detailed_feedback
    except SimulationFeedback.DoesNotExist:
        feedback = None

    template_indicators = simulation.template.indicators.all()
    identified_indicators = simulation.indicators_identified.all()

    context = {
        'simulation': simulation,
        'feedback': feedback,
        'template_indicators': template_indicators,
        'identified_indicators': identified_indicators,
    }
    return render(request, 'simulations/simulation_result.html', context)


@login_required
def simulation_history(request):
    """View user's simulation history."""
    simulations = Simulation.objects.filter(user=request.user).select_related('template')

    # Calculate statistics
    total = simulations.count()
    completed = simulations.filter(status='completed').count()
    avg_score = sum(s.score or 0 for s in simulations.filter(status='completed')) / completed if completed > 0 else 0

    context = {
        'simulations': simulations,
        'total': total,
        'completed': completed,
        'avg_score': round(avg_score, 1),
    }
    return render(request, 'simulations/simulation_history.html', context)
