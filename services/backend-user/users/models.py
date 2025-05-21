# services/backend-user/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    profile_picture = models.URLField(blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default='en')
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username']
    USERNAME_FIELD = 'username'