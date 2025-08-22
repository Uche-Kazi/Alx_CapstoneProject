# ~/Alx_CapstoneProject/users/urls.py

from django.urls import path
from .views import UserRegistrationView # Assuming you'll create this view

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    # You'll add more URLs here for user-related actions like profile, etc.
]
