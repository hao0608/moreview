from django import forms

from movie.models import Movie

class MovieModelForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields = '__all__'
        