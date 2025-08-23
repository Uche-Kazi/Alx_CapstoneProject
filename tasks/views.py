# ~/Alx_CapstoneProject/tasks/views.py

from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer

# --- Custom Permission ---
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read permissions are allowed for any authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS).
        # This part still allows any authenticated user to READ, but get_queryset will filter.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the owner of the object.
        return obj.owner == request.user

# --- Task API Views ---

class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all tasks or create a new task.
    - Requires authentication.
    - Users can only see their own tasks.
    - When creating a task, the owner is automatically set to the authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access

    def get_queryset(self):
        """
        Filters the queryset to return only tasks belonging to the authenticated user.
        """
        return Task.objects.filter(owner=self.request.user).order_by('due_date', 'created_at')

    def perform_create(self, serializer):
        """
        Sets the owner of the task to the currently authenticated user
        when a new task is created.
        """
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific task.
    - Requires authentication.
    - Users can only retrieve their own tasks.
    - Only the owner can update or delete their task.
    """
    # NO 'queryset = Task.objects.all()' here, we will define get_queryset instead.
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self): # <--- ADDED: Filter queryset for detail view
        """
        Filters the queryset to return only tasks belonging to the authenticated user.
        """
        return Task.objects.filter(owner=self.request.user)

