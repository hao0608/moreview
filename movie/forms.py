from django import forms
from movie.models import Movie, Tag


class MovieModelForm(forms.ModelForm):
    
    class Meta:
        model = Movie
        # fields = "__all__"

        fields = [
            "tag_id",
            "name",
            "content",
            "official_site",
            "time",
            "grade",
            "date_released",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "content": forms.Textarea(attrs={"class": "tinymceTextarea"}),
            "official_site": forms.TextInput(attrs={"class": "form-control"}),
            "time": forms.TextInput(attrs={"class": "form-control"}),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "date_released": forms.TextInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
