from django.shortcuts import render
from django.urls import reverse

from .forms import ReviewModelForm
from django.views.generic import (
    CreateView,
)

from review.models import Review
from .forms import ReviewModelForm

# Create your views here.
class ReviewCreateView(CreateView):
    model = Review
    template_name = "review/review_create_form.html"
    form_class = ReviewModelForm


    
