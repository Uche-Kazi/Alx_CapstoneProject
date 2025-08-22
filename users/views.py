# ~/Alx_CapstoneProject/users/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer # We will create this next

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Allow any user to register

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for user registration.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

