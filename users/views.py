# from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.urls.base import reverse_lazy

from moreview import settings
from .forms import RegisterForm
from .models import User


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


class UserListView(UserPassesTestMixin, ListView):
    template_name = "user_list.html"
    model = User
    login_url = reverse_lazy('users:login')

    def test_func(self):
        return self.request.user.is_superuser
