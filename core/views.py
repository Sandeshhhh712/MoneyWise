from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.contrib.auth import login as authenticate
from .models import User
from .form import RegisterUserForm, LoginForm

# Create your views here.

def RegisterUserView(request:HttpRequest):
    form=RegisterUserForm()
    data={"form":form}
    if request.method=="POST":
        password=request.POST.get('password')
        hashed_password=make_password(password)
        clone=request.POST.copy()
        clone['password']=hashed_password
        form=RegisterUserForm(clone)
        if form.is_valid():
            form.save()
        return render(request, 'register.html', context=form)
    return render(request, 'register.html', data)


def LoginView(request:HttpRequest):
    form=LoginForm()
    if request.method=="POST":
        password=request.POST.get('password')
        email=request.POST.get('email')
        user=authenticate(email=email, password=password)
        if user==None:
            return render(request, 'login.html', {"form":form, "error":" Invalid email or password"})
        
        return redirect()
