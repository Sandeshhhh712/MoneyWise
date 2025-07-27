from django.urls import path
from .views import RegisterUserView, LoginView, ExpenseView, IncomeView, SavingsView,IndexView, TransactionView,LogoutView, EditExpenseView

urlpatterns = [
    path('register/', RegisterUserView, name="Register"),
    path('login/', LoginView, name='Login'),
    path('expense/', ExpenseView, name='Expense'),
    path('income/', IncomeView, name='Income'),
    path('savings/', SavingsView, name='Savings'),
    path('transactions/', TransactionView, name='Transaction'),
    path('logout/', LogoutView, name='Logout'),
    path('editexpense/<int:pk>', EditExpenseView, name='Edit_Expense'),
    path('', IndexView, name='Index')
]
