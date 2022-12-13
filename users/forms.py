from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput,
        max_length=128,
        validators=[validate_password],
    )
    confirm_password = forms.CharField(
        label=_("confirm password"), widget=forms.PasswordInput(), max_length=128
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error("password", _("Password does not match confirm_password"))

        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class AdminCreateForm(forms.ModelForm):
    password = forms.CharField(
        label=_("password"), widget=forms.PasswordInput(), max_length=128
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
