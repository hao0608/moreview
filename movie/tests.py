from django.test import TestCase
from django.urls import reverse, resolve

from faker import Faker
from .views import (
    MovieListView,
    MovieCreateView,
    MovieDeleteView,
    MovieDetailView,
    MovieEditView,
)

# Create your tests here.


'''
class MovieListViewTest(TestCase):
    view=MovieListView()
    def test_template_is_correct(self):
        self.assertEquals("movie_list.html",self.view.template_name)
        
class MovieDetailViewTest(TestCase):
    view=MovieDetailView()
    def test_template_is_correct(self):
        self.assertEquals("movie_detail.html",self.view.template_name)

class MovieCreateViewTest(TestCase):
    view=MovieCreateView()
    def test_template_is_correct(self):
        self.assertEquals("movie_create_form.html",self.view.template_name)

class MovieDeleteViewTest(TestCase):
    view=MovieDeleteView()


class MovieEditViewTest(TestCase):
    view=MovieEditView()
    def test_template_is_correct(self):
        self.assertEquals("movie_edit_form.html",self.view.template_name)
"""
