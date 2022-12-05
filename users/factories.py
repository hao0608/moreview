from moreview.factories import BaseFactory
from django.contrib.auth.hashers import make_password
from .models import User


class UserFactory(BaseFactory):
    model = User

    def __init__(self):
        super().__init__()
        self.data = {
            **dict.fromkeys(["username", "first_name"], self.faker.first_name()),
            "last_name": self.faker.last_name(),
            "email": self.faker.safe_email(),
            "password": make_password("password"),
        }

    def is_superuser(self):
        self.data.update({"is_superuser": True})
        return self

    def inactive(self):
        self.data.update({"is_active": False})
        return self
