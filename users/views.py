# from django.shortcuts import render
from django.contrib.auth.views import LoginView


# Create your views here.
class UserLoginView(LoginView):
    template_name = "login.html"
'''
class UserLogoutView(LogoutView):
    
class UserRegisterView(RegisterView):
    template_name = "register.html"

class UserProfileView(ProfileView):
    template_name ="profile.html"

class UserListView(UserListView):
    tmplate_name = "user_list.html"
'''
