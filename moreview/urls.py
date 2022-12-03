"""moreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from movie.views import (
    MovieListView,
    MovieCreateView,
    MovieDetailView,
    MovieEditView,
    MovieDeleteView,
)

urlpatterns = [
    path("base", TemplateView.as_view(template_name="base.html")),
    path("users/login", TemplateView.as_view(template_name="login.html")),
    path("users/user_list", TemplateView.as_view(template_name="user_list.html")),
    path("users/profile", TemplateView.as_view(template_name="profile.html")),
    path("users/register", TemplateView.as_view(template_name="register.html")),
    path("admin/", admin.site.urls),
    path("movies/create", MovieCreateView.as_view(), name="movie_create_form"),
    path("", MovieListView.as_view(), name="movie_list"),
    path("movies/<int:pk>", MovieDetailView.as_view(), name="movie_detail"),
    path("movies/<int:pk>/edit", MovieEditView.as_view(), name="movie_edit"),
    path("movies/<int:pk>/delete", MovieDeleteView.as_view(), name="movie_delete"),
]
