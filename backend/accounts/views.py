from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import CustomUser
from blogs.mongodb_service import mongodb_service


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # Check if user with this email already exists
    email = request.data.get('email')
    if email and CustomUser.objects.filter(email=email).exists():
        return Response({
            'error': 'User with this email already exists. Please login instead.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Save to MongoDB
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }
        mongodb_service.save_user(user_data)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Registration successful!'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Enhanced login with better error handling and performance optimization
    """
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            # Authenticate user with better error handling
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    
                    # Cache user data for faster subsequent requests
                    from django.core.cache import cache
                    cache_key = f"user_data_{user.id}"
                    user_data = UserSerializer(user).data
                    cache.set(cache_key, user_data, timeout=300)  # Cache for 5 minutes
                    
                    return Response({
                        'user': user_data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': 'Login successful!'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Account is disabled. Please contact support.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'error': 'Invalid email or password. Please check your credentials.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Please provide valid email and password.',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Login error: {str(e)}")
        return Response({
            'error': 'Login service temporarily unavailable. Please try again.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get user profile with caching for better performance
    """
    try:
        # Try to get from cache first
        from django.core.cache import cache
        cache_key = f"user_data_{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        # If not in cache, get from database and cache it
        serializer = UserSerializer(request.user)
        user_data = serializer.data
        cache.set(cache_key, user_data, timeout=300)  # Cache for 5 minutes
        
        return Response(user_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Profile error: {str(e)}")
        return Response({
            'error': 'Unable to retrieve profile. Please try again.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_demo_password(request):
    """Temporary endpoint to reset demo user password - remove after use"""
    try:
        user = CustomUser.objects.get(email='demo@gmail.com')
        user.set_password('12345678')
        user.save()
        return Response({'message': 'Demo user password reset successfully'})
    except CustomUser.DoesNotExist:
        # Create the user if it doesn't exist
        user = CustomUser.objects.create_user(
            email='demo@gmail.com',
            username='demo',
            password='12345678'
        )
        return Response({'message': 'Demo user created successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
