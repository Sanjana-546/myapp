import logging

logger = logging.getLogger(__name__)


class UserActivityTrackingMiddleware:
    """
    Middleware to track user activities for analytics and security monitoring.
    Note: Database tracking disabled - logs to logger instead.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only track authenticated users
        if not request.user.is_authenticated:
            return response
        
        # Determine action based on request
        action = self._determine_action(request, response)
        
        if action:
            logger.info(
                f"User Activity: {request.user.username} - {action} | "
                f"Path: {request.path} | Method: {request.method} | "
                f"IP: {self._get_client_ip(request)}"
            )
        
        return response
    
    def _determine_action(self, request, response):
        """Determine the action type based on request and response."""
        path = request.path
        method = request.method
        
        # JWT token actions
        if '/api/token/' in path:
            if method == 'POST':
                return 'login'
        elif '/api/token/refresh/' in path:
            return 'refresh_token'
        elif '/api/token/verify/' in path:
            return 'verify_token'
        
        # Dashboard views
        if '/dashboard/' in path:
            return 'view_dashboard'
        elif '/admin-dashboard/' in path:
            return 'view_dashboard'
        
        # Post actions
        if '/post/create/' in path and method == 'POST':
            return 'create_post'
        elif '/post/' in path and '/edit/' in path and method == 'POST':
            return 'edit_post'
        elif '/post/' in path and '/delete/' in path and method == 'POST':
            return 'delete_post'
        elif '/post/' in path and method == 'GET':
            return 'view_post'
        
        return None
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
