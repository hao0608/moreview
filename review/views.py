from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import ReviewModelForm
from django.views.generic import (
    CreateView,
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from movie.models import Movie
from review.models import Review
from .forms import ReviewModelForm

# Create your views here.
# class ReviewCreateView(CreateView):
#     model = Review
#     template_name = "review_create_form.html"
#     form_class = ReviewModelForm
    
class ReviewCreateView(View):
    form_class = ReviewModelForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
        movie=Movie.objects.get(id=request.POST['movieID'])
        user=User.objects.get(id=request.POST['userID'])
        content=request.POST['content']
        rating=int(request.POST['rating'])
        Review.objects.create(
            user=user,
            movie=movie,
            content=content,
            rating=rating
        )
        return HttpResponseRedirect(reverse("movie:detail", kwargs={"pk": movie.pk}))



    
