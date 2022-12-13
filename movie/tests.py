import time

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from faker import Faker
from movie.models import Movie, Tag
from movie.factories import MovieFactory, TagFactory
from movie.views import *


# Create your tests here.
class MovieModelTest(TestCase):
    faker = Faker()

    def setUp(self):
        self.tag = Tag.objects.create(name="test")
        self.movie = Movie.objects.create(
            tag_id=self.tag,
            name="test",
            content="test content",
            official_site="test url",
            time=120,
            image="test.jpg",
            grade="普遍級",
            date_released="2022-12-12",
        )

    def test_date_updated_field_updates_when_record_updates(self):
        self.movie.name = self.faker.name()
        time.sleep(1)
        self.movie.save()

        self.assertNotEqual(
            self.movie.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            self.movie.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        )


class MovieCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.view = MovieCreateView()
        self.client = Client()

    def test_template_is_correct(self):
        self.assertEqual("movie_create_form.html", self.view.template_name)

    def test_movie_create_page_can_render(self):
        response = self.client.get(reverse("movie:create"))
        self.assertEqual(200, response.status_code)

    def test_form_contains_correct_fields(self):
        self.assertEqual(
            [
                "tag_id",
                "name",
                "content",
                "official_site",
                "time",
                "grade",
                "date_released",
                "image",
            ],
            self.view.form_class.Meta.fields,
        )


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

    def setUp(self):
        self.tag = Tag.objects.create(name="test")
        self.movie = Movie.objects.create(
            tag_id=self.tag,
            name="test",
            content="test content",
            official_site="test url",
            time=120,
            image="test.jpg",
            grade="普遍級",
            date_released="2022-12-12",
        )

    def test_template_is_correct(self):
        self.assertEqual("movie_detail.html", self.view.template_name)

    def test_detail_page_can_render(self):
        response = self.client.get(
            reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )
        self.assertEqual(200, response.status_code)


class MovieDeleteViewTest(TestCase):
    client = Client()
    view = MovieDeleteView

    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="test")
        self.movie = Movie.objects.create(
            tag_id=self.tag,
            name="delete test",
            content="test content",
            official_site="test url",
            time=120,
            image="test.jpg",
            grade="普遍級",
            date_released="2022-12-12",
        )

    def test_success_url_is_correct(self):
        self.assertEqual(reverse("movie:manage-list"), self.view.success_url)

    def test_delete_can_work(self):
        response = self.client.post(
            reverse("movie:delete", kwargs={"pk": self.movie.id})
        )

        self.assertRedirects(response, expected_url=reverse("movie:manage-list"))
        self.assertEqual(0, Movie.objects.filter(name="delete test").count())


class MovieEditViewTest(TestCase):
    client = Client()
    view = MovieEditView

    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="test")
        self.movie = Movie.objects.create(
            tag_id=self.tag,
            name="test",
            content="test content",
            official_site="test url",
            time=120,
            image="test.jpg",
            grade="普遍級",
            date_released="2022-12-12",
        )

    def test_template_is_correct(self):
        self.assertEqual("movie_edit_form.html", self.view.template_name)

    def test_detail_page_can_render(self):
        response = self.client.get(reverse("movie:edit", kwargs={"pk": self.movie.pk}))
        self.assertEqual(200, response.status_code)
