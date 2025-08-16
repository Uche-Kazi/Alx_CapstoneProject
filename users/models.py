# ~/Alx_CapstoneProject/users/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email and username can be used for authentication.
    """
    def create_user(self, email, username, password, **extra_fields):
        """
        Create and save a User with the given email, username, and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom User model to allow email and username for authentication.
    The default username field from AbstractUser is used, and email is unique.
    """
    email = models.EmailField(_('email address'), unique=True) # Email is still unique

    # Use username for login primarily, but our custom backend will allow email too.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # Email is now a required field when creating users

    objects = CustomUserManager() # Assign the custom manager

    def __str__(self):
        return self.username or self.email # Represent by username or email
