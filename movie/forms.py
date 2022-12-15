from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.utils.translation import gettext as _

from movie.models import Movie


class MovieModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "tag_id",
            "name",
            "content",
            "official_site",
            AppendedText("time", _("minutes")),
            "grade",
            "date_released",
            "image",
        )

    class Meta:
        model = Movie
        fields = [
            "tag_id",
            "name",
            "content",
            "official_site",
            "time",
            "grade",
            "date_released",
            "image",
        ]
        widgets = {
            "date_released": forms.TextInput(attrs={"type": "date"}),
        }
