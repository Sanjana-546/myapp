from django.utils import timezone

from ..permissions import is_site_admin


class LoginTrackingMiddleware:
    """
    Middleware to track user login sessions and enforce role-based access control.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track session start time for login tracking
        if request.user.is_authenticated and 'login_time' not in request.session:
            request.session['login_time'] = timezone.now().isoformat()
            request.session['user_role'] = 'admin' if is_site_admin(request.user) else 'author'

        response = self.get_response(request)
        return response
