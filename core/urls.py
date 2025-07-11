from django.urls import path
from .views import RegisterUserForm

urlpatterns = [
    path('register/', RegisterUserForm, name="Register"),
    path('login/')
]
