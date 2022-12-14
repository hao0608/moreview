from django.db import models
from django.urls import reverse
import datetime

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=10, default="搞笑")
    description = models.TextField(default="a")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


movie_grade = [
    ("普遍級", "普遍級"),
    ("保護級", "保護級"),
    ("輔12級", "輔12級"),
    ("輔15級", "輔15級"),
    ("限制級", "限制級"),
]


class Movie(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, default="1")
    name = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    official_site = models.TextField()
    time = models.IntegerField()
    image = models.ImageField(upload_to="movies/", blank=False, null=False)
    grade = models.TextField(null=False, blank=False, choices=movie_grade, default=1)
    date_released = models.DateField(
        default=datetime.date.today,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("movie:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
