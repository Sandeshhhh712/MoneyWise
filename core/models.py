from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(models.Model):
    id=models.BigAutoField(primary_key=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    Age=models.IntegerField(null=True)
    created_at=models.DateField(auto_now_add=True)

    