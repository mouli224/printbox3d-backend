from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration - simplified to essential fields only"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=True, max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'phone']
        extra_kwargs = {
            'first_name': {'required': True},
            'username': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Auto-generate username from email if not provided
        if not attrs.get('username'):
            attrs['username'] = attrs['email'].split('@')[0].lower().replace('.', '').replace('-', '')[:30]
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        phone = validated_data.pop('phone', None)  # Store phone for later if needed
        user = User.objects.create_user(**validated_data)
        # Note: Phone is not stored in User model by default. 
        # Add to user profile model if you create one later.
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login (supports email or username)"""
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('username'):
            raise serializers.ValidationError({"error": "Either email or username is required"})
        return attrs
