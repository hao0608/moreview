from django.db import models
from django.urls import reverse

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=10, default="搞笑")
    description = models.TextField(default="a")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


movie_grade = [
    ("普遍級", "普遍級"),
    ("保護級", "保護級"),
    ("輔12級", "輔12級"),
    ("輔15級", "輔15級"),
    ("限制級", "限制級"),
]


class Movie(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, default="1")
    name = models.CharField(default="a", max_length=20)
    content = models.TextField(default="a", max_length=500)
    official_site = models.TextField(default="a")
    time = models.TextField(default="a")
    # grade = models.TextField(default="普遍級")
    grade = models.TextField(null=False, blank=False, choices=movie_grade, default=1)

    date_released = models.DateField(
        default="2020-10-10",
    )
    # date_released = models.DateField(widget = forms.DateInput(attrs={'type':'date'}))

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # return reverse("movie_detail", kwargs={"id": self.id})
        return reverse("movie_list")
