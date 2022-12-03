from django.db import models

# Create your models here.
class review(models.Model):
    name = models.CharField(max_length=10, default="搞笑")
    description = models.TextField(default="a")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)