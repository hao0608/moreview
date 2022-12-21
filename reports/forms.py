from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.utils.translation import gettext as _

from .models import Report
from users.models import User


class ReportModelForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["content"]
