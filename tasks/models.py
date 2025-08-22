# ~/Alx_CapstoneProject/tasks/models.py

from django.db import models
from django.conf import settings # Import settings to reference AUTH_USER_MODEL

class Task(models.Model):
    """
    Represents a single To-Do task.
    """
    # Foreign Key to CustomUser model, links a task to its owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks', # Allows easy access to user's tasks: user.tasks.all()
        help_text="The user who owns this task."
    )
    title = models.CharField(
        max_length=200,
        help_text="A brief title for the task."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional detailed description of the task."
    )
    due_date = models.DateField(
        blank=True,
        null=True,
        help_text="Optional due date for the task."
    )
    is_completed = models.BooleanField(
        default=False,
        help_text="Indicates whether the task is completed or not."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the task was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the task was last updated."
    )

    class Meta:
        ordering = ['due_date', 'created_at'] # Default ordering for tasks
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        """
        String representation of the Task object.
        """
        return f"{self.title} (Owner: {self.owner.username})"
