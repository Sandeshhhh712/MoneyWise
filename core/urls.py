from django.urls import path
from .views import RegisterUserView, LoginView

urlpatterns = [
    path('register/', RegisterUserView, name="Register"),
    path('login/', LoginView, name='Login')
]
