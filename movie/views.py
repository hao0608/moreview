from django.shortcuts import render
from django.urls import reverse
from review.models import Review,Heart

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
    template_name = "movie_create_form.html"
    form_class = MovieModelForm


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(movie_id=self.object.id)  
        heart_list=Heart.objects.all()
        context['heart_list']=[]
        for heart in heart_list:
            if heart.user.id == self.request.user.id:
                for review in context["review_list"]:
                    if heart.review.id == review.id:
                        context["heart_list"].append(Heart.objects.get(user=self.request.user.id,review=review.id)) 
        return context


class MovieListView(ListView):
    model = Movie
    home_template_name = "homepage.html"
    manage_template_name = "movie_list.html"
    queryset = Movie.objects.filter(image__contains="movies/").order_by(
        "-date_released"
    )

    def get_template_names(self, *args, **kwargs):
        if self.request.path == reverse("movie:list"):
            return [self.home_template_name]
        else:
            return [self.manage_template_name]

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)

        if self.request.path == reverse("movie:list"):
            # 取得request
            query = self.request.GET.get("q")
            order = self.request.GET.get("order")
            order_query = "-date_released"
            movie_obj = None
            if order == "Asc":
                order_query = "date_released"

            if query is not None:  # 搜尋
                movie_obj = Movie.objects.filter(
                    name__contains=query, image__contains="movies/"
                ).order_by(order_query)
            else:  # 沒有搜尋
                movie_obj = Movie.objects.filter(image__contains="movies/").order_by(
                    order_query
                )
            context["object_list"] = movie_obj
            context["order"]=order
            return context
        else:
            # 取得request
            query = self.request.GET.get("q")
            movie_obj = None
            if query is not None:  # 搜尋
                movie_obj = Movie.objects.filter(name__contains=query)
            else:  # 沒有搜尋
                movie_obj = Movie.objects.all()
            context["object_list"] = movie_obj
            return context


class MovieEditView(UpdateView):
    form_class = MovieModelForm
    template_name = "movie_edit_form.html"
    queryset = Movie.objects.all()


class MovieDeleteView(DeleteView):
    model = Movie
    success_url = "/movies"

    def get_success_url(self):
        return reverse("movie:manage-list")
