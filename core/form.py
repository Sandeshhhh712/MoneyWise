from django import forms
from django.forms import widgets
from .models import User

class RegisterUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[ 'email','password','first_name', 'last_name', 'DOB']

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email', 'password']