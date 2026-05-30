from django.shortcuts import redirect
from django.urls import reverse


# URL prefixes that are always allowed through (no pre-assessment required)
ALLOWED_PREFIXES = (
    '/accounts/',       # login, logout, register
    '/assessments/',    # entire assessments app (pre-assessment + quiz flow)
    '/manage/',         # admin panel (staff only, but safe to allow)
    '/static/',
    '/media/',
    '/quiz/chatbot/',
)

ALLOWED_EXACT = (
    '/',
)


class PreAssessmentMiddleware:
    """
    Redirect first-time students to the pre-assessment before they can
    access any part of the student platform.

    Staff and superusers are never affected.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if (
            user.is_authenticated
            and not user.is_staff
            and not user.is_superuser
            and not user.pre_assessment_completed
        ):
            path = request.path

            # Allow whitelisted paths through
            allowed = (
                path in ALLOWED_EXACT
                or any(path.startswith(p) for p in ALLOWED_PREFIXES)
            )

            if not allowed:
                return redirect(reverse('assessments:pre_assessment'))

        return self.get_response(request)
