# from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse


# Create your views here.
class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    http_method_names = ["post"]

    def get_redirect_url(self):
        return ""
