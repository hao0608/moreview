from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin


# Create your models here.
class User(AbstractUser, DirtyFieldsMixin):
    date_updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super(User, self).save(*args, **kwargs)
