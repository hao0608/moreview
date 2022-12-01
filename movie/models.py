from django.db import models

# Create your models here.
class Tag(models.Model):
    name=models.TextField()
    description=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

class Movie(models.Model):
    # tag_id=models.ForeignKey(Tag, on_delete=models.CASCADE)
    name=models.TextField()
    content=models.TextField(max_length=500)
    official_site=models.TextField()
    time=models.TextField()
    grade=models.TextField()
    date_released=models.DateTimeField()
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies_movie"

