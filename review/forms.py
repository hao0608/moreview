from django import forms

from review.models import Review
from django.utils.translation import gettext as _


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]

        labels = {
            'rating': _("rating"),
            'content': _("review content")
        }

