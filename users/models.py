from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"))
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
