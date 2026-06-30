from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional user data."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['full_name'] = user.get_full_name()
        
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view with enhanced response."""
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def custom_token_verify(request):
    """Custom token verification endpoint."""
    from rest_framework_simplejwt.tokens import AccessToken
    
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'detail': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        access_token = AccessToken(token)
        access_token.check_backend()
        
        return Response({
            'valid': True,
            'user_id': access_token['user_id'],
            'exp': access_token['exp']
        })
    except Exception as e:
        return Response(
            {'valid': False, 'detail': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def protected_view(request):
    """Example protected view to test JWT authentication."""
    return Response({
        'message': 'This is a protected endpoint',
        'user': request.user.username if request.user.is_authenticated else 'Anonymous'
    })
