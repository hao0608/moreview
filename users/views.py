# from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from moreview import settings
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login, authenticate


# Create your views here.
class UserRegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save(commit=False)

        user.set_password(user.password)
        user.save()

        login(self.request, user)

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    http_method_names = ["post"]

    def get_redirect_url(self):
        return ""

class UserProfileView(FormView):
    template_name = "profile.html"
    form_class = ProfileForm
