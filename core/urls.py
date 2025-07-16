from django.urls import path
from .views import RegisterUserView, LoginView, ExpenseView, IncomeView, SavingsView

urlpatterns = [
    path('register/', RegisterUserView, name="Register"),
    path('login/', LoginView, name='Login'),
    path('expense/', ExpenseView, name="Expense"),
    path('income/', IncomeView, name='Income'),
    path('savings/', SavingsView, name='Savings')
]
