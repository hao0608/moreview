import time

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from faker import Faker
from users.factories import UserFactory
from .views import UserLoginView


# Create your tests here.
class UserModelTest(TestCase):
    faker = Faker()

    def test_date_updated_field_updates_when_record_updates(self):
        user = UserFactory().create()

        user.email = self.faker.unique.safe_email()
        # date_joined and date_updated is difference in nanoseconds when created
        time.sleep(1)
        user.save()

        self.assertNotEqual(
            user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
            user.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        )


class UserLoginViewTest(TestCase):
    view = UserLoginView()
    client = Client()
    user = None

    def setUp(self) -> None:
        self.user = UserFactory().create()

    def test_template_is_correct(self):
        self.assertEqual("login.html", self.view.template_name)

    def test_redirect_url_is_root(self):
        request = RequestFactory().post(
            reverse("users:login"),
            {"username": self.user.username, "password": "password"},
        )
        self.view.setup(request)

        self.assertIs("", self.view.get_redirect_url())

    def test_login_page_can_render(self):
        response = self.client.get(reverse("users:login"))

        self.assertIs(200, response.status_code)

    def test_user_can_login_and_redirect_to_home(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": self.user.username, "password": "password"},
        )

        self.assertRedirects(response, expected_url="/")

    def test_user_cannot_login_with_incorrect_certificate(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": self.user.username, "password": "secret"},
        )

        self.assertNotEqual(0, len(response.context["form"].errors))

    def test_inactive_user_cannot_login(self):
        inactive_user = UserFactory().inactive().create()

        response = self.client.post(
            reverse("users:login"),
            {"username": inactive_user.username, "password": "password"},
        )

        self.assertNotEqual(0, len(response.context["form"].errors))
