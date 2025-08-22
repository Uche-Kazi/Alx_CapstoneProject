# ~/Alx_CapstoneProject/users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserLoginSerializer # Import both serializers

# User Registration View
class UserRegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny] # Allow any user (even unauthenticated) to register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Registered Successfully. Now perform Login to get access token",
        }, status=status.HTTP_201_CREATED)

# User Login View
class UserLoginView(generics.GenericAPIView):
    """
    API view for user login.
    Allows existing users to log in and receive JWT access and refresh tokens.
    """
    serializer_class = UserLoginSerializer # Use the UserLoginSerializer
    permission_classes = [AllowAny] # Allow any user (even unauthenticated) to login

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] # Get the authenticated user from the serializer

        # Generate JWT tokens using the serializer's helper method
        tokens = serializer.get_jwt_token(user)

        return Response({
            "message": "Login Successful",
            "access": tokens['access'],
            "refresh": tokens['refresh'],
        }, status=status.HTTP_200_OK)

# Add other user-related views here as needed, e.g., UserProfileView, PasswordResetView, etc.
