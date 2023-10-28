from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_request, name="login-page"),
    path('logout/', views.logout_request, name="logout-page"),
    path('register/', views.RegisterUserView.as_view(), name="register-page"),

    ]
