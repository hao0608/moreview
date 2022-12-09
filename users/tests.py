import time

from django.contrib import auth
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from faker import Faker

from users.factories import UserFactory
from .models import User
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserListView, UserProfileView


# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()

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
        self.view = UserRegisterView()
        self.client = Client()

    def test_url_is_correct(self):
        self.assertURLEqual("/register", reverse("users:register"))

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
    def setUp(self) -> None:
        self.view = UserLoginView()
        self.client = Client()
        self.user = UserFactory().create()

    def test_url_is_correct(self):
        self.assertURLEqual("/login", reverse("users:login"))

    def test_template_is_correct(self):
        self.assertEqual("login.html", self.view.template_name)

    def test_redirect_url_is_root(self):
        request = RequestFactory().post(
            reverse("users:login"),
            {"username": self.user.username, "password": "Passw0rd!"},
        )
        self.view.setup(request)

        self.assertURLEqual("", self.view.get_redirect_url())

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
        self.view = UserLogoutView()
        self.client = Client()
        self.user = UserFactory().create()

    def test_url_is_correct(self):
        self.assertURLEqual("/logout", reverse("users:logout"))

    def test_only_allow_post_method(self):
        self.assertEqual(["post"], self.view.http_method_names)

    def test_user_can_logout_and_redirect_to_movies_list(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(reverse("users:logout"))

        self.assertRedirects(response, expected_url=reverse("movie:list"))


class UserListViewTest(TestCase):
    def setUp(self) -> None:
        self.view = UserListView()
        self.client = Client()
        self.admin = UserFactory().is_superuser().create()
        self.user = UserFactory().create()

    def test_url_ic_correct(self):
        self.assertEqual("/users", reverse("users:list"))

    def test_model_is_user_model(self):
        self.assertEqual(User, self.view.model)

    def test_template_name_is_correct(self):
        self.assertEqual("user_list.html", self.view.template_name)

    def test_redirect_login_url_is_correct(self):
        self.assertEqual(reverse("users:login"), self.view.login_url)

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse("users:list"))

        self.assertRedirects(
            response,
            expected_url=f"{reverse('users:login')}?next={reverse('users:list')}",
        )

    def test_user_is_forbidden_to_access(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(reverse("users:list"))
        self.assertEqual(403, response.status_code)

    def test_admin_can_view_page(self):
        self.client.login(username=self.admin.username, password="Passw0rd!")

        response = self.client.get(reverse("users:list"))

        self.assertEqual(200, response.status_code)


class UserProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.view = UserProfileView()
        self.client = Client()
        self.user = UserFactory().create()
        self.admin = UserFactory().is_superuser().create()

    def test_url_is_correct(self):
        self.assertURLEqual('/profile', reverse('users:profile'))

    def test_template_name_is_correct(self):
        self.assertEqual('profile.html', self.view.template_name)

    def test_model_is_correct(self):
        self.assertEqual(User, self.view.model)

    def test_unauthorized_user_redirects_to_login(self):
        response = self.client.get(reverse('users:profile'))

        self.assertRedirects(response, expected_url=f"{reverse('users:login')}?next={reverse('users:profile')}")

    def test_authorized_user_can_view_profile(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(200, response.status_code)

    def test_authorized_user_redirects_to_personal_profile_when_request_to_view_profile_with_parameter(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))

        self.assertRedirects(response, expected_url=reverse("users:profile"))

    def test_authorized_admin_can_view_other_user_profile(self):
        self.client.login(username=self.admin.username, password="Passw0rd!")

        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))

        self.assertEqual(200, response.status_code)
