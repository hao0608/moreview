from django.db import models
from users.models import User
from movie.models import Movie
from django.urls import reverse

# Create your models here.
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
review_rating = [
    (ONE, "1"),
    (TWO, "2"),
    (THREE, "3"),
    (FOUR, "4"),
    (FIVE, "5"),
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    rating = models.IntegerField(choices=review_rating, default=3)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    existed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("movie:detail", kwargs={"pk": self.movie.pk})


class Heart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
