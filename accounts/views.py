from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import User, UserProgress, LearningPath
from analytics.models import LearningAnalytics, UserActivity


class RegisterView(CreateView):
    """User registration view."""

    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create learning analytics record for new user
        LearningAnalytics.objects.create(user=self.object)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


def _post_login_redirect(user):
    """Return the correct redirect URL after login based on user role."""
    if user.is_staff or user.is_superuser:
        return 'admin_panel:dashboard'
    if not user.pre_assessment_completed:
        return 'assessments:pre_assessment'
    return 'education:dashboard'


def login_view(request):
    """Custom login view."""
    if request.user.is_authenticated:
        return redirect(_post_login_redirect(request.user))

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='login',
                description='User logged in'
            )
            # Update login count
            analytics, _ = LearningAnalytics.objects.get_or_create(user=user)
            analytics.login_count += 1
            analytics.save()
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(_post_login_redirect(user))
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """User profile view."""
    user = request.user
    progress_records = UserProgress.objects.filter(user=user).select_related('module')
    learning_paths = LearningPath.objects.filter(user=user)

    try:
        analytics = user.learning_analytics
    except LearningAnalytics.DoesNotExist:
        analytics = LearningAnalytics.objects.create(user=user)

    context = {
        'user': user,
        'progress_records': progress_records,
        'learning_paths': learning_paths,
        'analytics': analytics,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def progress_view(request):
    """View user's learning progress."""
    user = request.user
    progress_records = UserProgress.objects.filter(user=user).select_related('module')

    # Calculate completion percentage
    total_modules = progress_records.count()
    completed_modules = progress_records.filter(completed=True).count()
    completion_percentage = (completed_modules / total_modules * 100) if total_modules > 0 else 0

    context = {
        'progress_records': progress_records,
        'total_modules': total_modules,
        'completed_modules': completed_modules,
        'completion_percentage': completion_percentage,
    }
    return render(request, 'accounts/progress.html', context)
