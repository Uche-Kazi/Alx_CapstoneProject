# ~/Alx_CapstoneProject/todo_list_api/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # API endpoints for user authentication (registration, login, logout)
    path('api/users/', include('users.urls')),

    # API endpoints for tasks
    path('api/tasks/', include('tasks.urls')),

    # JWT Authentication Endpoints
    # Obtains a new access token and refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refreshes an access token using a refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Verifies an access token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
