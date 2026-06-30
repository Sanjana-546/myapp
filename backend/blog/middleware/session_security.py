from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone


class SessionSecurityMiddleware:
    """
    Middleware to enhance session security and manage session timeouts.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for expired sessions
        if request.user.is_authenticated and 'login_time' in request.session:
            login_time = request.session.get('login_time')
            if login_time:
                try:
                    from datetime import datetime
                    login_dt = datetime.fromisoformat(login_time)
                    session_duration = (timezone.now() - login_dt).total_seconds()
                    
                    # Session timeout: 24 hours
                    if session_duration > 86400:
                        logout(request)
                        return redirect('blog:user_login')
                except (ValueError, TypeError):
                    pass

        response = self.get_response(request)
        return response
