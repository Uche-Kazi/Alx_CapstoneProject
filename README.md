CAPSTONE PROJECT: "To-Do List API"

Week 4 Achievements: User Authentication & Task Permissions

This document outlines the features and configurations implemented during Week 4, focusing on establishing a robust user authentication system using JSON Web Tokens (JWT) and securing task management endpoints with object-level permissions.

1. Custom User Model (users/models.py)
A custom user model (CustomUser) was implemented to extend Django's default user functionality, allowing for more flexible authentication (e.g., using email and username for login).

Model: CustomUser inherited from AbstractUser.

Fields: email was made unique and required, username was retained.

Manager: A custom manager (CustomUserManager) was created to handle the creation of users and superusers, specifically for the custom user model.

settings.py Configuration: AUTH_USER_MODEL = 'users.CustomUser' was set to tell Django to use this custom model.

2. User Authentication Backend (users/backends.py)
A custom authentication backend (EmailOrUsernameModelBackend) was created to allow users to log in using either their email or username along with their password.

This backend integrates with Django's authenticate function.

settings.py Configuration: AUTHENTICATION_BACKENDS was updated to include this custom backend:

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

3. User Registration Endpoint
A robust API endpoint for user registration was implemented.

Serializer (users/serializers.py): UserRegisterSerializer was created:

Inherits from serializers.ModelSerializer for the CustomUser model.

Includes username, email, password, and password2 (for confirmation).

validate method ensures password and password2 match.

create method handles hashing the password before saving the user.

View (users/views.py): UserRegisterView was created:

Inherits from generics.CreateAPIView.

Uses UserRegisterSerializer.

permission_classes = [permissions.AllowAny] ensures anyone can register.

Returns a 201 Created status upon successful registration.

URLs (users/urls.py & todo_list_api/urls.py):

users/urls.py defines path('register/', UserRegisterView.as_view(), name='register').

todo_list_api/urls.py includes this app's URLs: path('api/users/', include('users.urls')).

4. JWT-Based User Login Endpoint
A secure API endpoint for user login was implemented, issuing JWT access and refresh tokens.

settings.py Configuration (Crucial for JWT):

'rest_framework_simplejwt' was added to INSTALLED_APPS.

REST_FRAMEWORK settings were configured to use JWTAuthentication:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # For browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT settings were added to define token lifetimes and other JWT-specific configurations.

Serializer (users/serializers.py): UserLoginSerializer was created:

Inherits from serializers.Serializer (not ModelSerializer).

Includes username and password.

validate method uses django.contrib.auth.authenticate to verify credentials.

Includes a get_jwt_token helper method to generate JWT tokens upon successful authentication.

View (users/views.py): UserLoginView was created:

Inherits from generics.GenericAPIView.

Uses UserLoginSerializer.

permission_classes = [permissions.AllowAny] ensures anyone can attempt to log in.

Upon valid credentials, it returns a 200 OK status with access and refresh tokens.

URLs (users/urls.py): users/urls.py defines path('login/', UserLoginView.as_view(), name='login').

5. Task Management Endpoints with Permissions
The task management API endpoints were secured to ensure proper access control.

Custom Permission (tasks/views.py): IsOwnerOrReadOnly was created:

Inherits from permissions.BasePermission.

Allows GET, HEAD, OPTIONS (read-only) requests for any authenticated user.

Restricts PUT, PATCH, DELETE (write/delete) requests to only the owner of the task (obj.owner == request.user).

Task List & Create View (tasks/views.py): TaskListCreateAPIView was modified:

permission_classes = [permissions.IsAuthenticated] ensures only logged-in users can list or create tasks.

get_queryset() was overridden to return Task.objects.filter(owner=self.request.user). This ensures users can only see tasks they own when requesting the task list.

perform_create() was overridden to automatically set the owner of a new task to request.user.

Task Detail View (tasks/views.py): TaskRetrieveUpdateDestroyAPIView was modified:

permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly] applies both general authentication and object-level ownership checks.

get_queryset() was overridden to return Task.objects.filter(owner=self.request.user). This is crucial for security, as it prevents non-owners from even retrieving a task by its ID (resulting in a 404 Not Found for tasks they don't own).

6. URL Routing for Tasks (tasks/urls.py & todo_list_api/urls.py)
The URL patterns for the tasks app were configured to properly map to the views and avoid conflicts.

tasks/urls.py:

path('', views.TaskListCreateAPIView.as_view(), name='task-list-create') to handle GET (list) and POST (create) requests for /api/tasks/.

path('<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail') to handle GET, PUT, PATCH, DELETE requests for specific tasks like /api/tasks/1/.

todo_list_api/urls.py:

path('api/tasks/', include('tasks.urls')) correctly includes the tasks app's URLs under the /api/tasks/ prefix.

7. Testing with Postman
Postman was extensively used to test all implemented API endpoints:

User Registration (POST /api/users/register/): Confirmed 201 Created status.

User Login (POST /api/users/login/): Confirmed 200 OK status with access and refresh JWT tokens.

Unauthorized Task Access (GET /api/tasks/ without token): Confirmed 401 Unauthorized.

Authenticated Task List (GET /api/tasks/ with valid token): Confirmed 200 OK with a list of user's tasks (initially empty).

Authenticated Task Creation (POST /api/tasks/ with valid token): Confirmed 201 Created with owner automatically assigned.

Authenticated Task Retrieval (Owner) (GET /api/tasks/<id>/ with owner's token): Confirmed 200 OK with task details.

Authenticated Task Retrieval (Non-owner) (GET /api/tasks/<id>/ with non-owner's token): Confirmed 404 Not Found (due to queryset filtering).

Authenticated Task Update (Non-owner) (PATCH /api/tasks/<id>/ with non-owner's token): Confirmed 404 Not Found.

Authenticated Task Update (Owner) (PATCH /api/tasks/<id>/ with owner's token): Confirmed 200 OK with updated task details.

This documentation provides a clear overview of the robust and secure foundation I've built for my Capstone Project: "To-Do List API", during Week 4.