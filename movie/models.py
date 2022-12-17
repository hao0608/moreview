import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.
class Tag(models.Model):
    name = models.CharField(_("name"), max_length=10)
    description = models.TextField(_("description"))
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
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name=_("tag"))
    name = models.CharField(_("name"), max_length=20)
    content = models.TextField(_("content"), max_length=500)
    official_site = models.URLField(_("official site"))
    time = models.PositiveSmallIntegerField(_("time"))
    image = models.ImageField(_("image"), upload_to="movies/")
    grade = models.TextField(_("grade"), choices=movie_grade)
    date_released = models.DateField(_("release date"), default=datetime.date.today)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("movie:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
