import time

from django.contrib import auth
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from faker import Faker

from users.factories import UserFactory
from .models import User
from .views import UserRegisterView, UserLoginView, UserLogoutView


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


class UserRegisterViewTest(TestCase):
    def setUp(self) -> None:
        self.view = UserRegisterView
        self.client = Client()

    def test_template_name_is_correct(self):
        self.assertEqual("register.html", self.view.template_name)

    def test_form_contains_correct_fields(self):
        self.assertEqual(
            [
                "username",
                "email",
                "password",
                "confirm_password",
                "last_name",
                "first_name",
            ],
            self.view.form_class.Meta.fields,
        )

    def test_success_url_is_correct(self):
        self.assertEqual(reverse("movie:list"), self.view.success_url)

    def test_register_page_can_render(self):
        response = self.client.get(reverse("users:register"))

        self.assertEqual(200, response.status_code)

    def test_user_can_register_and_auto_login(self):
        user = UserFactory().data.copy()
        user.pop("password")

        response = self.client.post(
            reverse("users:register"),
            {**user, "password": "Passw0rd!", "confirm_password": "Passw0rd!"},
        )

        self.assertRedirects(response, expected_url=reverse("movie:list"))
        self.assertEqual(1, User.objects.filter(**user).count())
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_user_cannot_register_when_confirm_password_not_match_password(self):
        user = UserFactory().data.copy()
        user.pop("password")

        response = self.client.post(
            reverse("users:register"),
            {**user, "password": "Passw0rd!", "confirm_password": "password"},
        )

        self.assertFormError(
            response.context["form"],
            field="password",
            errors=[_("Password does not match confirm_password")],
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
            {"username": self.user.username, "password": "Passw0rd!"},
        )
        self.view.setup(request)

        self.assertIs("", self.view.get_redirect_url())

    def test_login_page_can_render(self):
        response = self.client.get(reverse("users:login"))

        self.assertIs(200, response.status_code)

    def test_user_can_login_and_redirect_to_movies_list(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": self.user.username, "password": "Passw0rd!"},
        )

        self.assertRedirects(response, expected_url=reverse("movie:list"))

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


class UserLogoutViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.view = UserLogoutView
        self.user = UserFactory().create()

    def test_only_allow_post_method(self):
        self.assertEqual(['post'], self.view.http_method_names)

    def test_user_can_logout_and_redirect_to_movies_list(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(reverse("users:logout"))

        self.assertRedirects(response, expected_url=reverse("movie:list"))
