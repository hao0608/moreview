from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

# Create your models here.
class Review(models.Model):
    user_id = models.ManyToManyField(
            User,
            through='Heart',
            through_fields=('review_id', 'user_id')
        )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(default="a")
    rating = models.CharField(max_length=10, default="5")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Heart(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
