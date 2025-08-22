# ~/Alx_CapstoneProject/users/urls.py

from django.urls import path
from .views import UserRegisterView, UserLoginView # Import your user authentication views

app_name = 'users' # Namespace for the users app URLs

urlpatterns = [
    # User Registration API endpoint
    path('register/', UserRegisterView.as_view(), name='register'),
    # User Login API endpoint
    path('login/', UserLoginView.as_view(), name='login'),
    # Add other user-related API endpoints here (e.g., logout, profile update)
]