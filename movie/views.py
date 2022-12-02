from django.shortcuts import render

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .forms import MovieModelForm
from movie.models import Movie

# Create your views here.
class MovieCreateView(CreateView):
    model=Movie
    template_name='movie/movie_create_form.html'
    form_class= MovieModelForm


class MovieDetailView(DetailView):
    model=Movie
    template_name='movie/movie_detail.html'
    

class MovieListView(ListView):
    model = Movie
    template_name='movie/movie_list.html'

