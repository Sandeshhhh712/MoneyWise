from django import forms
from .models import User, Expense,Income, Savings

class RegisterUserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=[ 'first_name', 'last_name', 'age','email','password']

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email', 'password']


class ExpenseForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model=Expense
        fields=['category', 'amount', 'description']


class IncomeForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model=Income
        fields=['amount', 'description']


class SavingsForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model=Savings
        fields=['category', 'amount', 'description']
