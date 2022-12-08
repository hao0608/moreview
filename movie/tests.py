import time

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from faker import Faker
import datetime
from movie.models import Movie
from movie.factories import MovieFactory, TagFactory
from movie.views import *


# Create your tests here.
class MovieModelTest(TestCase):
    faker = Faker()

    def test_date_updated_field_updates_when_record_updates(self):
        movie = MovieFactory().create()
        tag = TagFactory().create()

        movie.time = self.faker.random_int(100, 200)
        time.sleep(1)
        movie.save()

        self.assertNotEqual(
            movie.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            movie.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        )


class MovieCreateViewTest(TestCase):
    view = MovieCreateView()
    client = Client()

    def test_template_is_correct(self):
        self.assertEqual("movie_create_form.html", self.view.template_name)

    def test_movie_create_page_can_render(self):
        response = self.client.get(reverse("movie:create"))
        self.assertIs(200, response.status_code)

    # def test_movie_post(self):
    #     self.client.post('/movies/create', {'name':'test name', 'content': 'test content','official_site':'test url', 'time': 120 , 'image':'test.jpg', 'grade':'普遍級','date_released':datetime.date.today })
    #     self.assertEqual(Movie.objects.get(name='test name').content, "test content")

class MovieListViewTest(TestCase):
    view = MovieListView()
    client = Client()

    def test_homepage_template_is_correct(self):
        self.assertEqual("homepage.html", self.view.home_template_name)

    def test_manage_list_template_is_correct(self):
        self.assertEqual("movie_list.html", self.view.manage_template_name)

    def test_homepage_can_render(self):
        response = self.client.get(reverse("movie:list"))
        self.assertIs(200, response.status_code)
    
    def test_manage_list_page_can_render(self):
        response = self.client.get(reverse("movie:manage-list"))
        self.assertIs(200, response.status_code)

class MovieDetailViewTest(TestCase):
    view = MovieDetailView()
    client = Client()

    def test_template_is_correct(self):
        self.assertEqual("movie_detail.html", self.view.template_name)

    # def test_movie_create_page_can_render(self):
    #     response = self.client.get(reverse("movie:detail", self.movie.id))
    #     self.assertIs(200, response.status_code)