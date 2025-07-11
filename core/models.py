from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    email=models.EmailField(unique=True)
    DOB=models.DateField(null=True)
    created_at=models.DateField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name']