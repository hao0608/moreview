from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from review.models import Review, Heart
from django.db.models import Count, Avg, Func,IntegerField, Case, When

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from .forms import MovieModelForm
from review.forms import ReviewModelForm
from review.models import Review
from movie.models import Movie
from reports.models import Report
from reports.forms import ReportModelForm

# Create your views here.


class Round(Func):
    function = "Round"
    template = "%(function)s(%(expressions)s, 2)"


class MovieCreateView(UserPassesTestMixin,CreateView):
    model = Movie
    template_name = "movie_create_form.html"
    form_class = MovieModelForm
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.is_superuser


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context["form"]=ReviewModelForm()
        context["report_create_form"]=ReportModelForm()

        # movie average rating
        context["movie"] = Movie.objects.annotate(
            average_rating=Round(Avg(
                Case(
                    When(review__existed = False, then="review__rating"),
                    output_field=IntegerField()
                )))
        ).get(id=self.kwargs["pk"])

        # sort, default : "latest"
        order = self.request.GET.get("order")
        # According to date_created
        order_query = "-date_created"
        if order == "oldest":
            order_query = "date_created"

        review_list = (
            Review.objects.filter(movie_id=self.object.id)
            .annotate(heart_number=Count("heart"))
            .order_by(order_query)
        )

        # According to number of heart
        # highest
        if order == "heart_highest":
            review_list = (
                Review.objects.filter(movie_id=self.object.id)
                .annotate(heart_number=Count("heart"))
                .order_by("-heart_number")
            )
        # lowest
        elif order == "heart_lowest":
            review_list = (
                Review.objects.filter(movie_id=self.object.id)
                .annotate(heart_number=Count("heart"))
                .order_by("heart_number")
            )

        # According to rating
        # highest
        if order == "rating_highest":
            review_list = (
                Review.objects.filter(movie_id=self.object.id)
                .annotate(heart_number=Count("heart"))
                .order_by("-rating")
            )
        # lowest
        elif order == "rating_lowest":
            review_list = (
                Review.objects.filter(movie_id=self.object.id)
                .annotate(heart_number=Count("heart"))
                .order_by("rating")
            )

        context["review_list"] = review_list
        context["order"] = order

        # Displays the hearts that the user has clicked
        heart_list = Heart.objects.all()
        context["heart_list"] = []
        for heart in heart_list:
            if heart.user.id == self.request.user.id:
                for review in context["review_list"]:
                    if heart.review.id == review.id:
                        context["heart_list"].append(
                            Heart.objects.get(
                                user=self.request.user.id, review=review.id
                            )
                        )

        context["self_review_list"] = []
        for review in context["review_list"]:
            if self.request.user.id == review.user.id and review.existed != True:
                if not self.request.user.is_superuser:
                    context["self_review_list"].append(review)

        report_list = (Report.objects.filter(user=self.request.user.id))

        context["report_list"] = report_list
        context["self_report_list"] = []
        for report in report_list:
            for review in context["review_list"]:
                if report.review.id == review.id:
                    if not self.request.user.is_superuser:
                        context["self_report_list"].append(review)
        
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
            # get request
            query = self.request.GET.get("q")
            order = self.request.GET.get("order")
            order_query = "-date_released"
            movie_obj = None
            if order == "oldest":
                order_query = "date_released"

            if query is not None:  # search
                movie_obj = Movie.objects.filter(
                    name__contains=query, image__contains="movies/"
                ).order_by(order_query)
            else:  # not search
                movie_obj = Movie.objects.filter(image__contains="movies/").order_by(
                    order_query
                )
            context["object_list"] = movie_obj
            context["order"] = order
            
            return context
        else:
            # get request
            query = self.request.GET.get("q")
            movie_obj = None
            if query is not None:  # serch
                movie_obj = Movie.objects.filter(name__contains=query).order_by("-date_created")
            else:  # not search
                movie_obj = Movie.objects.all().order_by("-date_created")
            context["object_list"] = movie_obj
            return context


class MovieEditView(UserPassesTestMixin,UpdateView):
    form_class = MovieModelForm
    template_name = "movie_edit_form.html"
    queryset = Movie.objects.all()
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.is_superuser


class MovieDeleteView(UserPassesTestMixin,DeleteView):
    model = Movie
    success_url = "/movies"
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse("movie:manage-list")
