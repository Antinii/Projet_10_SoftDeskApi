from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the application
    """
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=128, blank=True)
    birthdate = models.DateField()

    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['username', 'birthdate']
