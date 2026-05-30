import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import User
from education.models import Category, Module, Lesson, Video, PhishingIndicator
from quiz.models import AdaptiveQuestion, AdaptiveQuizAttempt, UserKnowledgeProfile, AdminContentSubmission
from badges.models import Badge, UserBadge
from analytics.models import UserActivity, LearningAnalytics


def staff_required(view_func):
    """Decorator: only staff/superusers may access."""
    decorated = user_passes_test(
        lambda u: u.is_active and (u.is_staff or u.is_superuser),
        login_url='accounts:login'
    )(view_func)
    return login_required(decorated)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@staff_required
def dashboard(request):
    """Admin overview dashboard."""
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    active_today = UserActivity.objects.filter(
        timestamp__date=timezone.now().date()
    ).values('user').distinct().count()

    total_questions = AdaptiveQuestion.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()

    # Quiz stats
    attempts_today = AdaptiveQuizAttempt.objects.filter(
        started_at__date=timezone.now().date()
    ).count()
    avg_score = AdaptiveQuizAttempt.objects.filter(
        status='completed', score_percentage__isnull=False
    ).aggregate(avg=Avg('score_percentage'))['avg'] or 0

    # Level distribution
    level_dist = UserKnowledgeProfile.objects.values('estimated_level').annotate(
        count=Count('id')
    ).order_by('estimated_level')

    # Recent quiz attempts
    recent_attempts = AdaptiveQuizAttempt.objects.filter(
        status='completed'
    ).select_related('user', 'category').order_by('-completed_at')[:10]

    # Top students by score
    top_students = (
        AdaptiveQuizAttempt.objects
        .filter(status='completed', score_percentage__isnull=False)
        .values('user__username', 'user__id')
        .annotate(avg_score=Avg('score_percentage'), attempts=Count('id'))
        .order_by('-avg_score')[:5]
    )

    # ML chatbot status
    try:
        from ml_engine.models.chatbot import chatbot
        chatbot_status = {'trained': chatbot.is_trained, 'qa_count': len(chatbot.qa_pairs)}
    except Exception:
        chatbot_status = {'trained': False, 'qa_count': 0}

    context = {
        'total_users': total_users,
        'active_today': active_today,
        'total_questions': total_questions,
        'total_categories': total_categories,
        'attempts_today': attempts_today,
        'avg_score': round(avg_score, 1),
        'level_dist': list(level_dist),
        'recent_attempts': recent_attempts,
        'top_students': top_students,
        'chatbot_status': chatbot_status,
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ─── Students ─────────────────────────────────────────────────────────────────

@staff_required
def students(request):
    """List all student accounts with activity stats."""
    search = request.GET.get('q', '')
    level = request.GET.get('level', '')

    qs = User.objects.filter(is_staff=False, is_superuser=False)
    if search:
        qs = qs.filter(Q(username__icontains=search) | Q(email__icontains=search))

    students_list = qs.annotate(
        quiz_count=Count('adaptive_quiz_attempts', filter=Q(adaptive_quiz_attempts__status='completed')),
        avg_score=Avg('adaptive_quiz_attempts__score_percentage',
                      filter=Q(adaptive_quiz_attempts__status='completed')),
        badges_count=Count('earned_badges'),
    ).order_by('-date_joined')

    if level:
        # Filter by knowledge level (requires subquery)
        user_ids = UserKnowledgeProfile.objects.filter(
            estimated_level=level
        ).values_list('user_id', flat=True)
        students_list = students_list.filter(id__in=user_ids)

    return render(request, 'admin_panel/students.html', {
        'students': students_list,
        'search': search,
        'level': level,
    })


@staff_required
def student_detail(request, user_id):
    """Detailed view of a single student."""
    student = get_object_or_404(User, id=user_id, is_staff=False, is_superuser=False)
    profiles = UserKnowledgeProfile.objects.filter(user=student).select_related('category')
    attempts = AdaptiveQuizAttempt.objects.filter(
        user=student, status='completed'
    ).select_related('category').order_by('-completed_at')[:20]
    badges = UserBadge.objects.filter(user=student).select_related('badge')
    activities = UserActivity.objects.filter(user=student).order_by('-timestamp')[:15]

    return render(request, 'admin_panel/student_detail.html', {
        'student': student,
        'profiles': profiles,
        'attempts': attempts,
        'badges': badges,
        'activities': activities,
    })


@staff_required
def edit_student(request, user_id):
    """Update a student's profile details."""
    student = get_object_or_404(User, id=user_id, is_staff=False, is_superuser=False)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        if username and email:
            # Check username uniqueness (excluding this user)
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                messages.error(request, "That username is already taken.")
            elif User.objects.filter(email=email).exclude(id=user_id).exists():
                messages.error(request, "That email is already in use.")
            else:
                student.username = username
                student.email = email
                student.first_name = request.POST.get('first_name', '').strip()
                student.last_name = request.POST.get('last_name', '').strip()
                student.skill_level = request.POST.get('skill_level', student.skill_level)
                student.is_active = request.POST.get('is_active') == 'on'
                student.save()
                messages.success(request, f"Student '{student.username}' updated successfully.")
        else:
            messages.error(request, "Username and email are required.")
    return redirect('admin_panel:student_detail', user_id=user_id)


@staff_required
@require_POST
def delete_student(request, user_id):
    """Permanently delete a student account."""
    student = get_object_or_404(User, id=user_id, is_staff=False, is_superuser=False)
    username = student.username
    student.delete()
    messages.success(request, f"Student '{username}' has been deleted.")
    return redirect('admin_panel:students')


@staff_required
def change_student_password(request, user_id):
    """Admin reset of a student's password."""
    student = get_object_or_404(User, id=user_id, is_staff=False, is_superuser=False)
    if request.method == 'POST':
        password = request.POST.get('new_password', '').strip()
        confirm = request.POST.get('confirm_password', '').strip()
        if not password:
            messages.error(request, "Password cannot be empty.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        elif password != confirm:
            messages.error(request, "Passwords do not match.")
        else:
            student.set_password(password)
            student.save()
            messages.success(request, f"Password for '{student.username}' changed successfully.")
    return redirect('admin_panel:student_detail', user_id=user_id)


# ─── Content Management ───────────────────────────────────────────────────────

@staff_required
def content(request):
    """Content management: questions, categories, videos."""
    tab = request.GET.get('tab', 'modules')
    categories = Category.objects.all()

    questions = AdaptiveQuestion.objects.select_related('category').order_by(
        'category__sort_order', 'difficulty'
    )
    cat_filter = request.GET.get('category', '')
    diff_filter = request.GET.get('difficulty', '')
    if cat_filter:
        questions = questions.filter(category__slug=cat_filter)
    if diff_filter:
        questions = questions.filter(difficulty=diff_filter)

    videos = Video.objects.select_related('category').order_by('category__sort_order', 'sort_order')
    badges = Badge.objects.all()
    modules = Module.objects.select_related('category').order_by('category__sort_order', 'order')
    indicators = PhishingIndicator.objects.all().order_by('indicator_type', 'name')

    return render(request, 'admin_panel/content.html', {
        'tab': tab,
        'categories': categories,
        'questions': questions,
        'videos': videos,
        'badges': badges,
        'modules': modules,
        'indicators': indicators,
        'cat_filter': cat_filter,
        'diff_filter': diff_filter,
        'difficulty_choices': AdaptiveQuestion.DIFFICULTY_CHOICES,
        'module_type_choices': Module.MODULE_TYPE_CHOICES,
        'module_difficulty_choices': Module.DIFFICULTY_CHOICES,
        'indicator_type_choices': PhishingIndicator.INDICATOR_TYPE_CHOICES,
    })


@staff_required
@require_POST
def add_question(request):
    """AJAX: add a new question."""
    try:
        data = json.loads(request.body)
        cat = get_object_or_404(Category, slug=data['category_slug'])
        options = [data['opt_a'], data['opt_b'], data['opt_c'], data['opt_d']]
        q = AdaptiveQuestion.objects.create(
            category=cat,
            question=data['question'],
            options=options,
            correct_answer=int(data['correct_answer']),
            explanation=data.get('explanation', ''),
            difficulty=data['difficulty'],
            difficulty_parameter=float(data.get('difficulty_parameter', 0.5)),
            created_by=request.user,
        )
        return JsonResponse({'id': q.id, 'status': 'created'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@staff_required
@require_POST
def delete_question(request, question_id):
    """Delete a question."""
    q = get_object_or_404(AdaptiveQuestion, id=question_id)
    q.delete()
    messages.success(request, 'Question deleted.')
    return redirect('admin_panel:content')


@staff_required
@require_POST
def toggle_question(request, question_id):
    """Toggle question active/inactive."""
    q = get_object_or_404(AdaptiveQuestion, id=question_id)
    q.is_active = not q.is_active
    q.save()
    return JsonResponse({'is_active': q.is_active})


@staff_required
@require_POST
def add_video(request):
    """Add a new educational video."""
    try:
        cat = get_object_or_404(Category, slug=request.POST['category_slug'])
        Video.objects.create(
            category=cat,
            title=request.POST['title'],
            url=request.POST['url'],
            duration=request.POST.get('duration', ''),
            description=request.POST.get('description', ''),
        )
        messages.success(request, f'Video "{request.POST["title"]}" added.')
    except Exception as e:
        messages.error(request, str(e))
    from django.urls import reverse
    return redirect(reverse('admin_panel:content') + '?tab=videos')


@staff_required
@require_POST
def delete_video(request, video_id):
    """Delete a video."""
    v = get_object_or_404(Video, id=video_id)
    v.delete()
    messages.success(request, 'Video deleted.')
    from django.urls import reverse
    return redirect(reverse('admin_panel:content') + '?tab=videos')


# ─── ML Management ────────────────────────────────────────────────────────────

@staff_required
def ml_management(request):
    """ML model management page."""
    try:
        from ml_engine.models.chatbot import chatbot
        chatbot_status = {
            'trained': chatbot.is_trained,
            'qa_count': len(chatbot.qa_pairs),
        }
    except Exception:
        chatbot_status = {'trained': False, 'qa_count': 0}

    pending_submissions = AdminContentSubmission.objects.filter(
        status='pending'
    ).order_by('-created_at')

    approved_unfed = AdminContentSubmission.objects.filter(
        status='approved', fed_to_model=False, content_type='chatbot_qa'
    ).count()

    # Build a sample of current Q&A pairs for display
    try:
        from ml_engine.models.chatbot import chatbot
        sample_qa = chatbot.qa_pairs[:10]
    except Exception:
        sample_qa = []

    return render(request, 'admin_panel/ml_management.html', {
        'chatbot_status': chatbot_status,
        'pending_submissions': pending_submissions,
        'approved_unfed': approved_unfed,
        'sample_qa': sample_qa,
    })


@staff_required
@require_POST
def submit_chatbot_qa(request):
    """Admin submits new Q&A pair for the chatbot."""
    question = request.POST.get('question', '').strip()
    answer = request.POST.get('answer', '').strip()
    category = request.POST.get('category', 'general')

    if not question or not answer:
        messages.error(request, 'Both question and answer are required.')
        return redirect('admin_panel:ml_management')

    AdminContentSubmission.objects.create(
        submitted_by=request.user,
        content_type='chatbot_qa',
        content_data={'question': question, 'answer': answer, 'category': category, 'keywords': []},
        status='approved',  # admin-submitted items auto-approved
    )
    messages.success(request, 'Q&A pair submitted and queued for training.')
    return redirect('admin_panel:ml_management')


@staff_required
@require_POST
def feed_to_model(request):
    """Feed all approved Q&A submissions to the chatbot and retrain."""
    try:
        from ml_engine.models.chatbot import chatbot
        unfed = AdminContentSubmission.objects.filter(
            content_type='chatbot_qa', status='approved', fed_to_model=False
        )
        new_pairs = [s.content_data for s in unfed]
        if new_pairs:
            chatbot.add_qa_pairs(new_pairs)
            unfed.update(fed_to_model=True, fed_at=timezone.now())
            messages.success(request, f'Fed {len(new_pairs)} Q&A pair(s) to the chatbot. Model retrained.')
        else:
            messages.info(request, 'No new Q&A pairs to feed.')
    except Exception as e:
        messages.error(request, f'Training failed: {e}')
    return redirect('admin_panel:ml_management')


@staff_required
@require_POST
def retrain_difficulty_model(request):
    """Retrain the difficulty predictor from quiz attempt data."""
    try:
        from ml_engine.models.difficulty_predictor import DifficultyPredictor
        from ml_engine.data.seed_data import SEED_TRAINING_DATA

        # Build training data from real quiz attempts
        attempts = AdaptiveQuizAttempt.objects.filter(
            status='completed', score_percentage__isnull=False
        ).prefetch_related('answers__question')

        training_data = list(SEED_TRAINING_DATA)  # start with seed data
        for attempt in attempts:
            answers = attempt.answers.all()
            if not answers:
                continue
            recent_correct = sum(1 for a in answers if a.is_correct)
            recent_accuracy = recent_correct / len(answers) if answers else 0.5
            profile = UserKnowledgeProfile.objects.filter(
                user=attempt.user, category=attempt.category
            ).first()
            proficiency = profile.proficiency_score if profile else 0.5
            # Determine what difficulty level ended up being appropriate
            if attempt.score_percentage >= 75:
                # They did well — next difficulty should be harder
                scores = [0, 1, 2]  # beginner=0, intermediate=1, advanced=2
                d_map = {'beginner': 1, 'intermediate': 2, 'advanced': 2}
                target = d_map.get(attempt.estimated_level or 'beginner', 1)
            else:
                d_map = {'beginner': 0, 'intermediate': 0, 'advanced': 1}
                target = d_map.get(attempt.estimated_level or 'beginner', 0)
            diff_levels = ['beginner', 'intermediate', 'advanced']
            training_data.append({
                'proficiency_score': proficiency,
                'recent_accuracy': recent_accuracy,
                'num_answers': len(answers),
                'target_difficulty': diff_levels[target],
            })

        predictor = DifficultyPredictor()
        success = predictor.train(training_data)
        if success:
            messages.success(request, f'Difficulty predictor retrained on {len(training_data)} data points.')
        else:
            messages.warning(request, f'Not enough data to train ({len(training_data)} points, need ≥10).')
    except Exception as e:
        messages.error(request, f'Retraining failed: {e}')
    return redirect('admin_panel:ml_management')


@staff_required
@require_POST
def add_module(request):
    """Add a new learning module."""
    from django.utils.text import slugify
    try:
        cat = get_object_or_404(Category, slug=request.POST['category_slug'])
        title = request.POST['title'].strip()
        slug = slugify(title)
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while Module.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        Module.objects.create(
            title=title,
            slug=slug,
            description=request.POST.get('description', ''),
            category=cat,
            module_type=request.POST.get('module_type', 'general'),
            difficulty=request.POST.get('difficulty', 'beginner'),
            content=request.POST.get('content', ''),
            video_url=request.POST.get('video_url') or None,
            duration_minutes=int(request.POST.get('duration_minutes', 10)),
            points=int(request.POST.get('points', 10)),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, f'Module "{title}" created.')
    except Exception as e:
        messages.error(request, str(e))
    from django.urls import reverse
    return redirect(reverse('admin_panel:content') + '?tab=modules')


@staff_required
@require_POST
def toggle_module(request, module_id):
    """Toggle module active/inactive."""
    m = get_object_or_404(Module, id=module_id)
    m.is_active = not m.is_active
    m.save()
    return JsonResponse({'is_active': m.is_active})


@staff_required
@require_POST
def delete_module(request, module_id):
    """Delete a module."""
    m = get_object_or_404(Module, id=module_id)
    title = m.title
    m.delete()
    messages.success(request, f'Module "{title}" deleted.')
    from django.urls import reverse
    return redirect(reverse('admin_panel:content') + '?tab=modules')


@staff_required
@require_POST
def add_indicator(request):
    """Add a new phishing indicator."""
    name = request.POST.get('name', '').strip()
    indicator_type = request.POST.get('indicator_type', '').strip()
    description = request.POST.get('description', '').strip()
    example = request.POST.get('example', '').strip()
    severity = int(request.POST.get('severity', 1))
    if name and indicator_type and description:
        PhishingIndicator.objects.create(
            name=name, indicator_type=indicator_type,
            description=description, example=example, severity=severity
        )
        messages.success(request, f'Indicator "{name}" added.')
    else:
        messages.error(request, 'Name, type and description are required.')
    from django.urls import reverse
    return redirect(reverse('admin_panel:content') + '?tab=indicators')


@staff_required
@require_POST
def delete_indicator(request, indicator_id):
    """Delete a phishing indicator."""
    ind = get_object_or_404(PhishingIndicator, id=indicator_id)
    ind.delete()
    messages.success(request, 'Indicator deleted.')
    from django.urls import reverse
    return redirect(reverse('admin_panel:content') + '?tab=indicators')


# ─── Content Edit Views ───────────────────────────────────────────────────────

@staff_required
@require_POST
def edit_module(request, module_id):
    from django.urls import reverse
    m = get_object_or_404(Module, id=module_id)
    m.title = request.POST.get('title', m.title).strip() or m.title
    m.description = request.POST.get('description', m.description).strip()
    cat_slug = request.POST.get('category_slug', '')
    if cat_slug:
        cat = Category.objects.filter(slug=cat_slug).first()
        if cat:
            m.category = cat
    m.module_type = request.POST.get('module_type', m.module_type)
    m.difficulty = request.POST.get('difficulty', m.difficulty)
    m.duration_minutes = int(request.POST.get('duration_minutes', m.duration_minutes) or m.duration_minutes)
    m.points = int(request.POST.get('points', m.points) or m.points)
    m.order = int(request.POST.get('order', m.order) or 0)
    m.is_active = request.POST.get('is_active') == 'on'
    m.video_url = request.POST.get('video_url', '').strip() or None
    m.content = request.POST.get('content', m.content)
    m.save()
    messages.success(request, f'Module "{m.title}" updated.')
    return redirect(reverse('admin_panel:content') + '?tab=modules')


@staff_required
def edit_question(request, question_id):
    """AJAX: edit an existing question."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        q = get_object_or_404(AdaptiveQuestion, id=question_id)
        cat = get_object_or_404(Category, slug=data['category_slug'])
        q.question = data['question']
        q.category = cat
        q.difficulty = data['difficulty']
        q.options = [data['opt_a'], data['opt_b'], data['opt_c'], data['opt_d']]
        q.correct_answer = int(data['correct_answer'])
        q.difficulty_parameter = float(data.get('difficulty_parameter', 0.5))
        q.explanation = data.get('explanation', '')
        q.save()
        return JsonResponse({'status': 'updated', 'id': q.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@staff_required
@require_POST
def edit_video(request, video_id):
    from django.urls import reverse
    v = get_object_or_404(Video, id=video_id)
    cat_slug = request.POST.get('category_slug', '')
    if cat_slug:
        cat = Category.objects.filter(slug=cat_slug).first()
        if cat:
            v.category = cat
    v.title = request.POST.get('title', v.title).strip() or v.title
    v.url = request.POST.get('url', v.url).strip()
    v.duration = request.POST.get('duration', v.duration)
    v.description = request.POST.get('description', v.description)
    v.status = request.POST.get('status', v.status)
    v.save()
    messages.success(request, f'Video "{v.title}" updated.')
    return redirect(reverse('admin_panel:content') + '?tab=videos')


@staff_required
@require_POST
def edit_indicator(request, indicator_id):
    from django.urls import reverse
    ind = get_object_or_404(PhishingIndicator, id=indicator_id)
    ind.name = request.POST.get('name', ind.name).strip() or ind.name
    ind.indicator_type = request.POST.get('indicator_type', ind.indicator_type)
    ind.description = request.POST.get('description', ind.description).strip()
    ind.example = request.POST.get('example', ind.example).strip()
    ind.severity = int(request.POST.get('severity', ind.severity) or ind.severity)
    ind.save()
    messages.success(request, f'Indicator "{ind.name}" updated.')
    return redirect(reverse('admin_panel:content') + '?tab=indicators')


# ─── Blog Management ──────────────────────────────────────────────────────────

@staff_required
def blog_management(request):
    from blog.models import Post, Category as BlogCategory
    posts = Post.objects.select_related('author', 'category').order_by('-created_at')
    blog_categories = BlogCategory.objects.all()
    return render(request, 'admin_panel/blog_management.html', {
        'posts': posts,
        'blog_categories': blog_categories,
    })


@staff_required
@require_POST
def add_blog_post(request):
    from blog.models import Post, Category as BlogCategory
    from django.utils import timezone as tz
    title = request.POST.get('title', '').strip()
    if not title:
        messages.error(request, 'Title is required.')
        return redirect('admin_panel:blog_management')
    cat_id = request.POST.get('category_id', '')
    cat = BlogCategory.objects.filter(id=cat_id).first() if cat_id else None
    status = request.POST.get('status', 'draft')
    post = Post(
        title=title,
        author=request.user,
        category=cat,
        excerpt=request.POST.get('excerpt', '').strip(),
        content=request.POST.get('content', '').strip(),
        status=status,
        featured=request.POST.get('featured') == 'on',
    )
    if status == 'published':
        post.published_at = tz.now()
    post.save()
    messages.success(request, f'Post "{title}" created.')
    return redirect('admin_panel:blog_management')


@staff_required
@require_POST
def edit_blog_post(request, post_id):
    from blog.models import Post, Category as BlogCategory
    from django.utils import timezone as tz
    post = get_object_or_404(Post, id=post_id)
    title = request.POST.get('title', '').strip()
    if not title:
        messages.error(request, 'Title is required.')
        return redirect('admin_panel:blog_management')
    cat_id = request.POST.get('category_id', '')
    cat = BlogCategory.objects.filter(id=cat_id).first() if cat_id else None
    old_status = post.status
    new_status = request.POST.get('status', 'draft')
    post.title = title
    post.category = cat
    post.excerpt = request.POST.get('excerpt', '').strip()
    post.content = request.POST.get('content', '').strip()
    post.status = new_status
    post.featured = request.POST.get('featured') == 'on'
    if new_status == 'published' and old_status != 'published':
        post.published_at = tz.now()
    post.save()
    messages.success(request, f'Post "{post.title}" updated.')
    return redirect('admin_panel:blog_management')


@staff_required
@require_POST
def delete_blog_post(request, post_id):
    from blog.models import Post
    post = get_object_or_404(Post, id=post_id)
    title = post.title
    post.delete()
    messages.success(request, f'Post "{title}" deleted.')
    return redirect('admin_panel:blog_management')


@staff_required
@require_POST
def add_blog_category(request):
    from blog.models import Category as BlogCategory
    name = request.POST.get('name', '').strip()
    if name:
        BlogCategory.objects.get_or_create(name=name, defaults={
            'description': request.POST.get('description', ''),
            'icon': request.POST.get('icon', 'tag'),
        })
        messages.success(request, f'Blog category "{name}" added.')
    else:
        messages.error(request, 'Category name is required.')
    return redirect('admin_panel:blog_management')


@staff_required
@require_POST
def delete_blog_category(request, cat_id):
    from blog.models import Category as BlogCategory
    cat = get_object_or_404(BlogCategory, id=cat_id)
    name = cat.name
    cat.delete()
    messages.success(request, f'Blog category "{name}" deleted.')
    return redirect('admin_panel:blog_management')


@staff_required
def create_admin_user(request):
    """Admin list; only superusers can create/edit/delete."""
    admin_users = User.objects.filter(
        Q(is_staff=True) | Q(is_superuser=True)
    ).order_by('-date_joined')

    if request.method == 'POST':
        if not request.user.is_superuser:
            messages.error(request, 'Only superusers can create admin accounts.')
            return redirect('admin_panel:create_admin')

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        is_superuser = request.POST.get('is_superuser') == 'on'

        errors = []
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already taken.')
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        elif password != password2:
            errors.append('Passwords do not match.')
        if email and User.objects.filter(email=email).exists():
            errors.append('Email already in use.')

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name,
                is_staff=True, is_superuser=is_superuser,
            )
            messages.success(request, f'Admin user "{username}" created successfully.')
            return redirect('admin_panel:create_admin')

    return render(request, 'admin_panel/create_admin.html', {
        'admin_users': admin_users,
    })


@staff_required
def edit_admin_user(request, user_id):
    """Superuser-only: edit another admin account."""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can edit admin accounts.')
        return redirect('admin_panel:create_admin')

    target = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        target.first_name = request.POST.get('first_name', '').strip()
        target.last_name  = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        if email and email != target.email and User.objects.filter(email=email).exclude(id=target.id).exists():
            messages.error(request, 'Email already in use by another account.')
            return redirect('admin_panel:edit_admin', user_id=user_id)
        target.email = email
        target.is_superuser = request.POST.get('is_superuser') == 'on'
        new_pw = request.POST.get('new_password', '').strip()
        if new_pw:
            if len(new_pw) < 8:
                messages.error(request, 'New password must be at least 8 characters.')
                return redirect('admin_panel:edit_admin', user_id=user_id)
            target.set_password(new_pw)
        target.save()
        messages.success(request, f'Admin "{target.username}" updated.')
        return redirect('admin_panel:create_admin')

    return render(request, 'admin_panel/edit_admin.html', {'target': target})


@staff_required
@require_POST
def delete_admin_user(request, user_id):
    """Delete an admin user — superuser only."""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can delete admin accounts.')
        return redirect('admin_panel:create_admin')
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
    else:
        username = user.username
        user.delete()
        messages.success(request, f'Admin user "{username}" deleted.')
    return redirect('admin_panel:create_admin')


@staff_required
def admin_profile(request):
    """Admin can view and update their own profile."""
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        phone      = request.POST.get('phone_number', '').strip()

        if email and email != user.email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'That email is already in use by another account.')
            return redirect('admin_panel:admin_profile')

        user.first_name   = first_name
        user.last_name    = last_name
        user.email        = email or user.email
        user.phone_number = phone

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        # Optional password change
        new_pw  = request.POST.get('new_password', '')
        new_pw2 = request.POST.get('new_password2', '')
        if new_pw:
            if len(new_pw) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
                return redirect('admin_panel:admin_profile')
            if new_pw != new_pw2:
                messages.error(request, 'Passwords do not match.')
                return redirect('admin_panel:admin_profile')
            user.set_password(new_pw)
            user.save()
            messages.success(request, 'Password updated — please log in again.')
            return redirect('accounts:login')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_panel:admin_profile')

    return render(request, 'admin_panel/admin_profile.html', {'admin_user': user})


@staff_required
def api_platform_stats(request):
    """JSON stats for dashboard charts."""
    # Quiz attempts per day (last 14 days)
    from django.db.models.functions import TruncDate
    daily = (
        AdaptiveQuizAttempt.objects
        .filter(status='completed', completed_at__gte=timezone.now() - timezone.timedelta(days=14))
        .annotate(day=TruncDate('completed_at'))
        .values('day')
        .annotate(count=Count('id'), avg_score=Avg('score_percentage'))
        .order_by('day')
    )
    return JsonResponse({'daily_attempts': list(daily)}, safe=False)
