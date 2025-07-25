from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login , authenticate
from .models import User, Expense, Income, Savings
from .form import RegisterUserForm, LoginForm, ExpenseForm, IncomeForm, SavingsForm
from datetime import datetime, timedelta
from django.utils import timezone
from itertools import chain
from operator import itemgetter
from django.contrib import messages

# Create your views here.


def RegisterUserView(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            login(request, user)
            request.session['user_id'] = user.id 
            return redirect('Index')  # Replace with your homepage URL name
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            request.session['user_id'] = user.id 
            return redirect('Index')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')


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

                return redirect('Index')
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
                print("Hello")
                return redirect('Index')
        return render(request, 'income.html', context={"form":IncomeForm()})
    



def SavingsView(request:HttpRequest):
    form=SavingsForm()
    user_id=request.session.get('user_id')
    if user_id:
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
                return redirect('Index')
            else:
                print(form.errors)
        return render(request, 'savings.html', context={"form":form})
    



def IndexView(request:HttpRequest):
    user_id=request.session.get('user_id')
    if user_id:
        try:
            
            user=User.objects.get(id=user_id)
            expense=Expense.objects.filter(user_id=user)
            income=Income.objects.filter(user_id=user)
            savings=Savings.objects.filter(user_id=user)
            total_expense=sum(e.amount for e in expense)
            total_income=sum(i.amount for i in income)
            total_savings=sum(s.amount for s in savings)
            balance=total_income-total_expense

            today=timezone.now()
            first_day_this_month=today.replace(day=1)

            last_day_previous_month=first_day_this_month-timedelta(days=1)
            first_day_previous_month=last_day_previous_month.replace(day=1)

            expense_previous=Expense.objects.filter(user_id=user, created_at__range=(first_day_previous_month, last_day_previous_month))
            income_previous=Income.objects.filter(user_id=user,created_at__range=(first_day_previous_month, last_day_previous_month))
            savings_previous=Savings.objects.filter(user_id=user,created_at__range=(first_day_previous_month, last_day_previous_month))
            

            expense_today=Expense.objects.filter(user_id=user,created_at__range=(first_day_this_month, today))
            income_today=Income.objects.filter(user_id=user,created_at__range=(first_day_this_month, today))
            savings_today=Savings.objects.filter(user_id=user,created_at__range=(first_day_this_month, today))
            

            expense_total_previous=sum(e.amount for e in expense_previous)
            income_total_previous=sum(i.amount for i in income_previous)
            savings_total_previous=sum(s.amount for s in savings_previous)
            balance_previous=income_total_previous-expense_total_previous


            expense_total_today=sum(e.amount for e in expense_today)
            income_total_today=sum(i.amount for i in income_today)
            savings_total_today=sum(s.amount for s in savings_today)
            balance_today=income_total_today-expense_total_today


            if expense_total_previous==0 and expense_total_today==0:
                expense_percentage="No change in expense"
            
            elif expense_total_today==0:
                expense_percentage="No expense this month"
            
            elif expense_total_previous==0:
                expense_percentage="100% increase (no expense in previous month)"

            else:
                change=expense_total_today-expense_total_previous
                percentage=(change/expense_total_previous)*100
                if percentage<0:
                    expense_percentage=f"{percentage}% less than previous month"
                elif percentage>0:
                    expense_percentage=f"{percentage}% more than previous month"
                else:
                    expense_percentage="Same as last month"




            if income_total_previous==0 and income_total_today==0:
                income_percentage="No change in income"
            
            elif income_total_today==0:
                income_percentage="No income this month"
            
            elif income_total_previous==0:
                income_percentage="100% increase (no income in previous month)"

            else:
                change=income_total_today-income_total_previous
                percentage=(change/income_total_previous)*100
                if percentage<0:
                    income_percentage=f"{percentage}% less than previous month"
                elif percentage>0:
                    income_percentage=f"{percentage}% more than previous month"
                else:
                    income_percentage="Same as last month"



            if savings_total_previous==0 and savings_total_today==0:
                savings_percentage="No change in savings"
            
            elif savings_total_today==0:
                savings_percentage="No savings this month"
            
            elif savings_total_previous==0:
                savings_percentage="100% increase (no savings in previous month)"

            else:
                change=savings_total_today-savings_total_previous
                percentage=(change/savings_total_previous)*100
                if percentage<0:
                    savings_percentage=f"{percentage}% less than previous month"
                elif percentage>0:
                    savings_percentage=f"{percentage}% more than previous month"
                else:
                    savings_percentage="Same as last month"


            if balance_previous==0 and balance_today==0:
                balance_percentage="No change in balance"
            
            elif balance_today==0:
                balance_percentage="No savings this month"
            
            elif balance_previous==0:
                balance_percentage="100% increase (no savings in previous month)"

            else:
                change=balance_today-balance_previous
                percentage=(change/balance_previous)*100
                if percentage<0:
                    balance_percentage=f"{percentage}% less than previous month"
                elif percentage>0:
                    balance_percentage=f"{percentage}% more than previous month"
                else:
                    balance_percentage="Same as last month"
            
            recent_expense=Expense.objects.filter(user_id=user).order_by('-created_at')[:10]
            recent_income=Income.objects.filter(user_id=user).order_by('-created_at')[:10]


            expense_data=[
                {"amount":f"-{e.amount}", "category":e.category,"description":e.description, "created_at":e.created_at}
                for e in recent_expense
            ]

            income_data=[
                {"amount":f"+{i.amount}", "category":"Income","description":i.description, "created_at":i.created_at}
                for i in recent_income
            ]

            transaction=sorted(
                chain(income_data, expense_data),
                key=itemgetter('created_at'),
                reverse=True
            )

            return render(request, 'index.html', context={"user":user.first_name,"expense":total_expense, "income":total_income, "savings":total_savings, "balance":balance, "expense_percentage": expense_percentage, "income_percentage":income_percentage, "savings_percentage":savings_percentage, "balance_percentage":balance_percentage, "transaction":transaction})
        except User.DoesNotExist:
            return redirect('Login')    
    return redirect('Login')     