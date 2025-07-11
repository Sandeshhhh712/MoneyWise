from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from .models import User
from .form import RegisterUserForm, LoginForm


# Create your views here.


def RegisterUserView(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'register.html', context={"form":form})
        return render(request, 'register.html', context={"form":form})

    return render(request, 'register.html', {"form": form})



def LoginView(request:HttpRequest):
    form=LoginForm()
    if request.method=="POST":
        password=request.POST.get('password')
        email=request.POST.get('email')

        try:
            user=User.objects.get(email=email)
            if user==None:
                return render(request, 'login.html', {"form":form, "error":" Invalid username"})
            else:
                verify_password=check_password(password, user.password)
                if verify_password:
                    return redirect('Register')
                return render(request, 'login.html', context={"form":form, "error":"Incorrect password"})
        except:
            return render(request, 'login.html', {"form":form, "error":" Invalid username"})
        
        
    return render(request, 'login.html', context={"form":form})