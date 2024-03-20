from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the application
    """
    birthdate = models.DateField()

    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['birthdate']

    def __str__(self):
        return self.username