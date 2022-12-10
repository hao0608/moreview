import time

from django import forms
from django.contrib import auth
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from faker import Faker

from users.factories import UserFactory
from .forms import RegisterForm, AdminCreateForm
from .models import User
from .views import (
    UserRegisterView,
    UserLogoutView,
    UserListView,
    UserProfileView,
    AdminCreateView,
    UserDeleteView
)


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


class RegisterFormTest(TestCase):
    def setUp(self) -> None:
        self.form = RegisterForm()

    def test_model_is_correct(self):
        self.assertEqual(User, self.form.Meta.model)

    def test_fields_are_correct(self):
        self.assertEqual(
            [
                "username",
                "first_name",
                "last_name",
                "email",
                "password",
                "confirm_password",
            ],
            self.form.Meta.fields,
        )

    def test_first_name_field_has_correct_setting(self):
        field = self.form.fields["first_name"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("first name"), field.label)
        self.assertEqual(150, field.max_length)
        self.assertTrue(field.required)

    def test_last_name_field_has_correct_setting(self):
        field = self.form.fields["last_name"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("last name"), field.label)
        self.assertEqual(150, field.max_length)
        self.assertTrue(field.required)

    def test_email_field_has_correct_setting(self):
        field = self.form.fields["email"]

        self.assertEqual(forms.EmailField, field.__class__)
        self.assertEqual(_("email address"), field.label)
        self.assertEqual(254, field.max_length)
        self.assertTrue(field.required)

    def test_password_field_has_correct_setting(self):
        field = self.form.fields["password"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("password"), field.label)
        self.assertEqual(forms.PasswordInput, field.widget.__class__)
        self.assertEqual(128, field.max_length)
        self.assertTrue(field.required)

    def test_confirm_password_field_has_correct_setting(self):
        field = self.form.fields["confirm_password"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("confirm password"), field.label)
        self.assertEqual(forms.PasswordInput, field.widget.__class__)
        self.assertEqual(128, field.max_length)
        self.assertTrue(field.required)

    def test_validation_failed_when_password_and_confirm_password_mismatch(self):
        form = self.form.__class__(
            {"password": "password1", "confirm_password": "password2"}
        )

        self.assertFalse(form.is_valid())
        self.assertTrue(
            _("Password does not match confirm_password") in form["password"].errors
        )


class UserRegisterViewTest(TestCase):
    def setUp(self) -> None:
        self.view = UserRegisterView()
        self.client = Client()

    def test_url_is_correct(self):
        self.assertURLEqual("/register", reverse("users:register"))

    def test_template_name_is_correct(self):
        self.assertEqual("register.html", self.view.template_name)

    def test_form_class_is_correct(self):
        self.assertEqual(RegisterForm, self.view.form_class)

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

    def test_url_is_correct(self):
        self.assertEqual("/users", reverse("users:list"))

    def test_model_is_correct(self):
        self.assertEqual(User, self.view.model)

    def test_template_name_is_correct(self):
        self.assertEqual("user_list.html", self.view.template_name)

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
        self.assertURLEqual("/profile", reverse("users:profile"))

    def test_template_name_is_correct(self):
        self.assertEqual("profile.html", self.view.template_name)

    def test_model_is_correct(self):
        self.assertEqual(User, self.view.model)

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse("users:profile"))

        self.assertRedirects(
            response,
            expected_url=f"{reverse('users:login')}?next={reverse('users:profile')}",
        )

    def test_authenticated_user_can_view_profile(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(200, response.status_code)

    def test_authenticated_user_redirects_to_personal_profile_when_request_to_view_profile_with_parameter(
            self,
    ):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(
            reverse("users:profile", kwargs={"pk": self.user.pk})
        )

        self.assertRedirects(response, expected_url=reverse("users:profile"))

    def test_authenticated_admin_can_view_other_user_profile(self):
        self.client.login(username=self.admin.username, password="Passw0rd!")

        response = self.client.get(
            reverse("users:profile", kwargs={"pk": self.user.pk})
        )

        self.assertEqual(200, response.status_code)


class AdminCreateFormTest(TestCase):
    def setUp(self) -> None:
        self.form = AdminCreateForm()

    def test_model_is_correct(self):
        self.assertEqual(User, self.form.Meta.model)

    def test_fields_are_correct(self):
        self.assertEqual(
            [
                "username",
                "first_name",
                "last_name",
                "email",
                "password",
            ],
            self.form.Meta.fields,
        )

    def test_first_name_field_has_correct_setting(self):
        field = self.form.fields["first_name"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("first name"), field.label)
        self.assertEqual(150, field.max_length)
        self.assertTrue(field.required)

    def test_last_name_field_has_correct_setting(self):
        field = self.form.fields["last_name"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("last name"), field.label)
        self.assertEqual(150, field.max_length)
        self.assertTrue(field.required)

    def test_email_field_has_correct_setting(self):
        field = self.form.fields["email"]

        self.assertEqual(forms.EmailField, field.__class__)
        self.assertEqual(_("email address"), field.label)
        self.assertEqual(254, field.max_length)
        self.assertTrue(field.required)

    def test_password_field_has_correct_setting(self):
        field = self.form.fields["password"]

        self.assertEqual(forms.CharField, field.__class__)
        self.assertEqual(_("password"), field.label)
        self.assertEqual(forms.PasswordInput, field.widget.__class__)
        self.assertTrue(field.required)


class AdminCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.view = AdminCreateView()
        self.client = Client()
        self.user = UserFactory().create()
        self.admin = UserFactory().is_superuser().create()

    def test_url_is_correct(self):
        self.assertURLEqual("/users/create", reverse("users:create"))

    def test_model_is_correct(self):
        self.assertEqual(User, self.view.model)

    def test_template_name_suffix_is_correct(self):
        self.assertEqual("_create_form", self.view.template_name_suffix)

    def test_form_class_is_correct(self):
        self.assertEqual(AdminCreateForm, self.view.form_class)

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse("users:create"))

        self.assertRedirects(
            response,
            expected_url=f"{reverse('users:login')}?next={reverse('users:create')}",
        )

    def test_authenticated_user_is_forbidden(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(reverse("users:create"))

        self.assertEqual(403, response.status_code)

    def test_authenticated_admin_can_view(self):
        self.client.login(username=self.admin.username, password="Passw0rd!")

        response = self.client.get(reverse("users:create"))

        self.assertEqual(200, response.status_code)

    def test_authenticated_admin_can_create_and_new_admin_can_login(self):
        admin = UserFactory().data.copy()
        admin.pop("password")

        self.client.login(username=self.admin.username, password="Passw0rd!")
        response = self.client.post(
            reverse("users:create"), {**admin, "password": "Passw0rd!"}
        )

        self.assertRedirects(response, expected_url=reverse("users:list"))
        self.assertEqual(1, User.objects.filter(**admin, is_superuser=True).count())
        self.assertTrue(
            self.client.login(username=admin.get("username"), password="Passw0rd!")
        )


class UserDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.view = UserDeleteView
        self.client = Client()
        self.user = UserFactory().create()

    def test_url_is_correct(self):
        self.assertURLEqual('/users/delete', reverse('users:delete'))

    def test_model_is_correct(self):
        self.assertEqual(User, self.view.model)

    def test_form_class_is_correct(self):
        self.assertEqual(forms.Form, self.view.form_class)

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.post(reverse('users:delete'))

        self.assertRedirects(response, expected_url=f"{reverse('users:login')}?next={reverse('users:delete')}")

    def test_http_get_method_redirects_to_profile(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.get(reverse('users:delete'))

        self.assertRedirects(response, expected_url=reverse('users:profile'))

    def test_authenticated_user_can_delete_account_then_logout_and_redirect_to_homepage(self):
        self.client.login(username=self.user.username, password="Passw0rd!")

        response = self.client.post(reverse('users:delete'))

        self.assertRedirects(response, expected_url=reverse('movie:list'))
        self.assertEqual(1, User.objects.filter(pk=self.user.pk, is_active=False).count())
        self.assertFalse(auth.get_user(self.client).is_authenticated)
