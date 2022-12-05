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
from review.models import Review

# Create your views here.

class MovieCreateView(CreateView):
    model = Movie
    template_name = "movie/movie_create_form.html"
    form_class = MovieModelForm


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie/movie_detail.html"
    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(movie_id=self.object.id)   
        return context


class MovieListView(ListView):
    model = Movie
    template_name = "movie/movie_list.html"
    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        query_dict=self.request.GET
        query=query_dict.get("q")
        movie_obj = None
        if query is not None:
            query="%"+query+"%"
            movie_obj = Movie.objects.raw('SELECT * FROM movie_movie WHERE name LIKE %s',[query])
        else:
            movie_obj = Movie.objects.all()
        context['object_list'] = movie_obj
        return context

class MovieEditView(UpdateView):
    form_class = MovieModelForm
    template_name = "movie/movie_edit_form.html"
    queryset = Movie.objects.all()


class MovieDeleteView(DeleteView):
    model = Movie

    def get_success_url(self):
        return reverse("movie_list")
