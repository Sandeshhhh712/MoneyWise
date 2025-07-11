from django import forms
from django.forms import widgets
from .models import User

class RegisterUserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=[ 'first_name', 'last_name', 'Age','email','password']

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email', 'password']