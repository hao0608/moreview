from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.views import View

from users.models import User
from movie.models import Movie
from review.models import Review, Heart
from .forms import ReviewModelForm

# Create your views here.
class ReviewCreateView(View):
    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=request.POST["movieID"])
        user = User.objects.get(id=self.request.user.id)
        content = request.POST["content"]
        rating = int(request.POST["rating"])
        Review.objects.create(user=user, movie=movie, content=content, rating=rating)
        return HttpResponseRedirect(reverse("movie:detail", kwargs={"pk": movie.pk}))


class ReviewDeleteView(View):
    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=request.POST["movieID"])
        Review.objects.get(id=request.POST["reviewID"]).delete()

        return HttpResponseRedirect(reverse("movie:detail", kwargs={"pk": movie.pk}))


class ReviewEditView(View):
    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=request.POST["movieID"])
        content = request.POST["content"]
        rating = int(request.POST["rating"])
        Review.objects.filter(id=request.POST["reviewID"]).update(
            content=content, rating=rating
        )
        return HttpResponseRedirect(reverse("movie:detail", kwargs={"pk": movie.pk}))


class HeartView(View):
    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=request.POST["movieID"])
        review = Review.objects.get(id=request.POST["reviewID"])
        user = User.objects.get(id=self.request.user.id)
        post_keys = request.POST.keys()
        if "heart" in post_keys:
            Heart.objects.create(
                user=user,
                review=review,
            )
        else:
            Heart.objects.get(user=user, review=review).delete()

        return HttpResponseRedirect(reverse("movie:detail", kwargs={"pk": movie.pk}))
