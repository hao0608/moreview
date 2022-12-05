from django.shortcuts import render

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from review.models import Review
from .forms import ReviewModelForm

# Create your views here.
class ReviewCreateView(CreateView):
    model = Review
    template_name = "review/review_create_form.html"
    form_class = ReviewModelForm

