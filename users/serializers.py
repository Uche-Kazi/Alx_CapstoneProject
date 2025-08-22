# ~/Alx_CapstoneProject/users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Get the CustomUser model
User = get_user_model()

# User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}, # Ensure email is required
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # Add additional validation for password strength if desired
        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not part of the model
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        # Note: This is a Serializer, not a ModelSerializer, so no 'model' attribute.
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if not username and not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Incorrect credentials. Please try again.")

        if not user.is_active:
            raise serializers.ValidationError("This user account has been deactivated.")

        data["user"] = user
        return data

    def get_jwt_token(self, user):
        """
        Generates JWT tokens for the authenticated user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
