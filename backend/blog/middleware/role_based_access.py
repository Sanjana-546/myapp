from django.shortcuts import redirect

from ..permissions import is_site_admin


class RoleBasedAccessMiddleware:
    """
    Middleware to enforce role-based access control for protected routes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define protected routes and their required roles
        protected_routes = {
            'blog:create_post': ['author'],
            'blog:edit_post': ['author'],
            'blog:user_dashboard': ['author'],
            'blog:admin_dashboard': ['admin'],
        }

        # Check if current route requires specific role
        if hasattr(request, 'resolver_match') and request.resolver_match:
            route_name = request.resolver_match.url_name
            
            if route_name in protected_routes:
                required_roles = protected_routes[route_name]
                
                if not request.user.is_authenticated:
                    return redirect('blog:user_login')
                
                user_role = 'admin' if is_site_admin(request.user) else 'author'
                
                if user_role not in required_roles:
                    # Redirect to appropriate dashboard based on user role
                    if user_role == 'admin':
                        return redirect('blog:admin_dashboard')
                    else:
                        return redirect('blog:user_dashboard')

        response = self.get_response(request)
        return response
