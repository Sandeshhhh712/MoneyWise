from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from .models import User, Expense, Income, Savings
from .form import RegisterUserForm, LoginForm, ExpenseForm, IncomeForm, SavingsForm


# Create your views here.


def RegisterUserView(request:HttpRequest):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if User.objects.filter(email=request.POST.get('email')).exists():
            return render(request, 'register.html', context={"form":form, "error":"User with this email already exist"})
        else: 
            if form.is_valid():
                user:User = form.save(commit=False)
                user.password = make_password(form.cleaned_data['password'])
                user.save()
                return redirect('Login')
           
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
                    request.session['user_id'] = user.id
                    return redirect('Expense')
                return render(request, 'login.html', context={"form":form, "error":"Incorrect password"})
        except:
            return render(request, 'login.html', {"form":form, "error":" Invalid username"})
        
    return render(request, 'login.html', context={"form":form})


def ExpenseView(request:HttpRequest):
    form=ExpenseForm()
    user_id=request.session.get('user_id')
    if user_id is None:
        return redirect('Login')
    else:
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('Login')
        

        if request.method=="POST":
            form=ExpenseForm(request.POST)
            if form.is_valid():
                data:Expense=form.save(commit=False)
                data.user_id=user
                data.save()
                return redirect('Register')
        return render(request, 'expense.html', context={"form":form})
    


def IncomeView(request:HttpRequest):
    form=IncomeForm()
    user_id=request.session.get('user_id')
    if user_id==None:
        return redirect('Login')
    else:
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('Login')
        
        if request.method=="POST":
            form=IncomeForm(request.POST)
            if form.is_valid():
                data:Income=form.save(commit=False)
                data.user_id=user
                data.save()
                return redirect('register.html')
        return render(request, 'income.html', context={"form":form})
    



def SavingsView(request:HttpRequest):
    form=SavingsForm()
    user_id=request.session.get('user_id')
    if request.user.is_authenticated:
        return redirect('Login')
    else: 
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('Login')
        
        if request.method=="POST":
            form=SavingsForm(request.POST)
            if form.is_valid():
                data:Savings=form.save(commit=False)
                data.user_id=user
                data.save()
                return redirect('Register')
        return render(request, 'savings.html', context={"form":form})
    


    
                