# ~/Alx_CapstoneProject/tasks/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.conf import settings
from django.db import IntegrityError
from .models import Task
from .serializers import TaskSerializer
from users.models import CustomUser  # Import CustomUser model if needed for user-specific logic
from django.shortcuts import get_object_or_404


# --- Task API Views ---

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read permissions are allowed for any authenticated user.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all tasks or create a new task.
    - Requires authentication.
    - Users can only see their own tasks.
    - When creating a task, the owner is automatically set to the authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the queryset to return only tasks belonging to the authenticated user.
        """
        return Task.objects.filter(owner=self.request.user).order_by('due_date', 'created_at')

    def perform_create(self, serializer):
        """
        Sets the owner of the task to the authenticated user upon creation.
        """
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific task.
    - Requires authentication.
    - Only the owner can update or delete their task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """
        Ensures the owner cannot be changed during an update.
        """
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        """
        Deletes a task instance.
        """
        instance.delete()

# --- User-related API Views (if needed, example below) ---

class UserProfileAPIView(APIView):
    """
    API view to retrieve and update the authenticated user's profile.
    - Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Assuming CustomUser is the user model and has a serializer
        # from users.serializers import CustomUserSerializer # You'd need to create this
        # serializer = CustomUserSerializer(request.user)
        # return Response(serializer.data)
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "is_staff": request.user.is_staff,
            "date_joined": request.user.date_joined
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # Example for updating user profile (e.g., email or other fields)
        # You'd need a CustomUserSerializer with update capability
        # from users.serializers import CustomUserSerializer
        # serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User profile update not yet implemented in detail."}, status=status.HTTP_501_NOT_IMPLEMENTED)


class LogoutView(APIView):
    """
    API view for logging out a user.
    - Clears the session and token (if using Token authentication).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # If using Token authentication, delete the user's token
            # This requires 'rest_framework.authtoken' to be in INSTALLED_APPS
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            
            logout(request) # Clears the session
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Logout failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An API view for changing a user's password.
    Requires the user to be authenticated.
    """
    serializer_class = None # Define a serializer for password change
    model = CustomUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password automatically
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# You'll need to define a serializer for ChangePasswordView in users/serializers.py
# Example:
# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
