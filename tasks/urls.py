# ~/Alx_CapstoneProject/tasks/urls.py

from django.urls import path
from tasks import views

# Define app_name for namespacing URLs
app_name = 'tasks'

urlpatterns = [
    # URL for listing all tasks and creating a new task
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),

    # URL for retrieving, updating, or deleting a specific task by its ID
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
]
