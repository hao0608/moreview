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
# from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from movie import views


urlpatterns = [
    path("base", TemplateView.as_view(template_name="base.html")),
    path("", include("users.urls")),
    path("", views.MovieListView.as_view(), name="movie_list"),
    path("movies/<int:pk>", views.MovieDetailView.as_view(), name="movie_detail"),
    path("movies/create", views.MovieCreateView.as_view(), name="movie_create"),
    path("movies/<int:pk>/edit", views.MovieEditView.as_view(), name="movie_edit"),
    path("movies/<int:pk>/delete", views.MovieDeleteView.as_view(), name="movie_delete")
    
    # path("admin/", admin.site.urls),
]
