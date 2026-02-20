from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .auth_serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully!',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT tokens (supports email or username)"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data['password']
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        user = None
        if email:
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        elif username:
            user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful!',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    return Response(UserSerializer(request.user).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update current user profile including shipping address"""
    user = request.user
    data = request.data

    for field in ['first_name', 'last_name', 'email']:
        if field in data:
            setattr(user, field, data[field])
    user.save()

    profile, _ = UserProfile.objects.get_or_create(user=user)
    for field in ['phone', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_pincode']:
        if field in data:
            setattr(profile, field, data[field])
    profile.save()

    return Response({
        'message': 'Profile updated successfully!',
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user"""
    return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Send a password reset email."""
    email = request.data.get('email', '').strip().lower()
    if not email:
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'message': 'If that email is registered, a reset link has been sent.'})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    frontend_url = getattr(settings, 'FRONTEND_URL', 'https://www.printbox3d.com')
    reset_url = f"{frontend_url}/reset-password/{uid}/{token}/"

    try:
        send_mail(
            subject='Reset Your PrintBox3D Password',
            message=(
                f"Hi {user.first_name or user.username},\n\n"
                f"Click the link below to reset your password. "
                f"This link expires in 24 hours.\n\n"
                f"{reset_url}\n\n"
                f"If you didn't request this, ignore this email.\n\n"
                f"— PrintBox3D Team"
            ),
            from_email=settings.EMAIL_HOST_USER or 'noreply@printbox3d.com',
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {e}")

    return Response({'message': 'If that email is registered, a reset link has been sent.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password using uid + token from the email link."""
    uid = request.data.get('uid', '')
    token = request.data.get('token', '')
    new_password = request.data.get('new_password', '')

    if not uid or not token or not new_password:
        return Response({'error': 'uid, token and new_password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 6:
        return Response({'error': 'Password must be at least 6 characters.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except Exception:
        return Response({'error': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Reset link has expired or already been used.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password reset successfully! You can now log in.'})
