from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("register", views.UserRegisterView.as_view(), name="register"),
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", views.UserLogoutView.as_view(), name="logout"),
    path("users", views.UserListView.as_view(), name="list"),
    path("profile", views.UserProfileView.as_view(), name="profile"),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name="profile"),
    path('profile/edit', views.ProfileUpdateView.as_view(), name='edit-profile'),
    path("users/create", views.AdminCreateView.as_view(), name="create"),
    path("users/delete", views.UserDeleteView.as_view(), name="delete"),
]
