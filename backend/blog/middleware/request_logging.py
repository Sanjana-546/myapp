import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Middleware to log all incoming requests for monitoring and debugging.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        logger.info(
            f"Request: {request.method} {request.path} | "
            f"IP: {self._get_client_ip(request)} | "
            f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'} | "
            f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')[:100]}"
        )
        
        response = self.get_response(request)
        
        # Log response details
        logger.info(
            f"Response: {response.status_code} | "
            f"Path: {request.path}"
        )
        
        return response
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
