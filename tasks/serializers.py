# ~/Alx_CapstoneProject/tasks/serializers.py

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Converts Task model instances to JSON and validates input for Task creation/updates.
    """
    # Make owner read-only as it will be set automatically by the view based on the authenticated user.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        # List all fields you want to expose through the API
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'due_date',
            'is_completed',
            'created_at',
            'updated_at'
        ]
        # Make some fields read-only for output, not for input
        read_only_fields = ['created_at', 'updated_at']
