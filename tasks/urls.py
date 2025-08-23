# ~/Alx_CapstoneProject/tasks/urls.py

from django.urls import path
from . import views # Changed to '.' for relative import which is common

app_name = 'tasks' # Namespace for the URLs

urlpatterns = [
    # URL for listing all tasks and creating a new task
    # This will now match /api/tasks/
    path('', views.TaskListCreateAPIView.as_view(), name='task-list-create'),

    # URL for retrieving, updating, or deleting a specific task by its ID
    # This will now match /api/tasks/<int:pk>/
    path('<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
]