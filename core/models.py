from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(models.Model):
    id=models.BigAutoField(primary_key=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    password=models.CharField()
    email=models.EmailField(unique=True)
    age=models.IntegerField()
    created_at=models.DateField(auto_now_add=True)


class ExpenseCategory(models.TextChoices):
    Food="food and dining", "Food And Dining",
    Entertainment="entertainment", "Entertainment",
    Rent="rent", "Rent",
    Transportation="transportation", "Transportation",
    Education="education", "Education",
    Medical="medical", "Medical",
    Groceries="groceries", "Groceries",
    Maintenance="maintenance", "Maintenance",
    Utilities="utilities", "Utilities",
    Travel="travel", "Travel",
    Loan="loan payment", "Loan Payment",
    Insurance="insurance", "Insurance",
    Shopping="shopping", "Shopping",
    Gadgets="gadgets", "Gadgets",
    Stationary="stationary", "Stationary"


class Expense(models.Model):
    id=models.BigAutoField(primary_key=True)
    category=models.CharField(max_length=300, choices=ExpenseCategory.choices, null=True)
    amount=models.IntegerField()
    description=models.TextField(blank=True, null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)


class Income(models.Model):
    id=models.BigAutoField(primary_key=True)
    amount=models.IntegerField()
    description=models.TextField(blank=True, null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)


class Savings(models.Model):
    id=models.BigAutoField(primary_key=True)
    category=models.CharField(max_length=300, choices=ExpenseCategory.choices, null=True)
    amount=models.IntegerField()
    description=models.TextField(blank=True, null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
