from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

from .forms import MeetingSystemLoginForm, RegisterUserForm

# Create your views here.


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = MeetingSystemLoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('Username')
            password = form.cleaned_data.get('Password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print('authenticated successfully!')
                print(user.profile.is_banned)

                if not user.profile.is_banned:
                    login(request, user)

                    return redirect("/")

                messages.error(request, "Аккаунт был заблокирован администратором",
                               extra_tags="bg-danger text-light rounded ps-2 message-box-login-error")

            else:
                messages.error(request, "Неверно введены имя и/или пароль", extra_tags="bg-warning rounded ps-2 message-box-login-error")
        else:
            messages.error(request, "Неверно введены имя и/или пароль", extra_tags="message-box-login-error")

    context = {
        "MeetingSystemLoginForm": MeetingSystemLoginForm,
    }

    return render(request, "Registration_Login_App/Event_Schedule_App_Login_Page.html", context=context)


def logout_request(request):
    logout(request)

    return redirect('/')


class RegisterUserView(FormView):
    form_class = RegisterUserForm
    template_name = "Registration_Login_App/Event_Schedule_App_Register_Page.html"
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],

        )

        login(self.request, user)

        return super(RegisterUserView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # something = something
    #     context['RegisterUserForm'] = self.form_class
    #     context['name'] = "Igor1"
    #     return context


