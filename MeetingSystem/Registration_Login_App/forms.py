from django import forms
from django.contrib.auth.models import User


class MeetingSystemLoginForm(forms.Form):
    Username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"placeholder": "Имя пользователя",
                                                             "name": "username",
                                                             "class": "form-control mt-2 mb-2"}), max_length=255)

    Password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Пароль",
                                                                 "name": "password",
                                                                 "class": "form-control mt-2 mb-2"}), max_length=100)


class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

        widgets = {
            "username": forms.TextInput(attrs={'type': 'text', 'class': 'form-control mt-2 mb-2', 'required': 'required'}),
            "email": forms.TextInput(attrs={'type': 'email', 'class': 'form-control mt-2 mb-2', 'required': 'required'}),
            "password": forms.TextInput(attrs={'type': 'password', 'class': 'form-control mt-2 mb-2', 'required': 'required'}),
        }


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

        widgets = {
            "username": forms.TextInput(attrs={'type': 'text', 'class': 'form-control mt-2', 'required': 'required'}),
            "first_name": forms.TextInput(attrs={'type': 'text', 'class': 'form-control mt-2', 'required': 'required'}),
            "last_name": forms.TextInput(attrs={'type': 'text', 'class': 'form-control mt-2', 'required': 'required'}),
            "email": forms.EmailInput(attrs={'type': 'text', 'class': 'form-control mt-2', 'required': 'required'}),

        }

