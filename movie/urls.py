from django.urls import path


from . import views

app_name = "movie"
urlpatterns = [
    path("", views.MovieListView.as_view(), name="list"),
    path("movies", views.MovieListView.as_view(), name="manage-list"),
    path("movies/<int:pk>", views.MovieDetailView.as_view(), name="detail"),
    path("movies/create", views.MovieCreateView.as_view(), name="create"),
    path("movies/<int:pk>/edit", views.MovieEditView.as_view(), name="edit"),
    path("movies/<int:pk>/delete", views.MovieDeleteView.as_view(), name="delete"),
]
