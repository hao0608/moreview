from django.shortcuts import render
from django.urls import reverse

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from .forms import MovieModelForm
from movie.models import Movie

# Create your views here.
class MovieCreateView(CreateView):
    model = Movie
    template_name = "movie/movie_create_form.html"
    form_class = MovieModelForm


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie/movie_detail.html"


class MovieListView(ListView):
    model = Movie
    template_name = "movie/movie_list.html"


class MovieEditView(UpdateView):
    form_class = MovieModelForm
    template_name = "movie/movie_edit_form.html"
    queryset = Movie.objects.all()


class MovieDeleteView(DeleteView):
    model = Movie

    def get_success_url(self):
        return reverse("movie_list")
