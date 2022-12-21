from django import forms

from review.models import Review


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = {"rating","content" }
