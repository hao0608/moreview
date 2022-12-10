from django import forms
from .models import User
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

class ProfileForm(forms.ModelForm):
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput(attrs={'disabled':'disabled', 'value': "password"}),
    )
    username = forms.CharField(
        label=_("username"),
        widget=forms.TextInput(attrs={'disabled':'disabled', 'width':'100%'}),
    )
    class Meta:
        model = User
        fields = [
            "username",
            "last_name",
            "first_name",
            "email",
            "password",
        ]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput,
        max_length=128,
        validators=[validate_password],
    )
    confirm_password = forms.CharField(
        label=_("confirm_password"), widget=forms.PasswordInput(), max_length=128
    )

    class Meta:
        model = User
        fields = [
            "username",
            "last_name",
            "first_name",
            "email",
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error("password", _("Password does not match confirm_password"))

        return cleaned_data
