from django.urls import path

from . import views

app_name = "users"
urlpatterns = [path("login", views.UserLoginView.as_view(), name="login"),
        #path("logout", views.UserLogoutView.as_view(), name="logout"),
        #path("register", views.UserRegisterView.as_view(), name="register"),
        #path("profile", views.UserProfileView.as_view(), name="profile"),
        #path("user_list", views.UserListView.as_view(), name="user_list")
        ]
