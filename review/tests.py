from django.test import TestCase, Client
from django.urls import reverse
import time

from faker import Faker
from movie.models import Movie, Tag
from review.models import Review, Heart
from review.views import *
from users.factories import UserFactory

# Create your tests here.
class ReviewModelTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = UserFactory().create()
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
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            content="test",
        )

    def test_data_updated_field_updates_when_record_updates(self):
        self.review.content = self.faker.text()
        time.sleep(1)
        self.review.save()

        self.assertNotEqual(
            self.review.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            self.review.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def test_reviews_will_be_deleted_when_the_movie_deleted(self):
        self.movie.delete()
        review_count = Review.objects.filter(id=self.review.id).count()

        self.assertEqual(0, review_count)


class HeartModelTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = UserFactory().create()
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
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            content="test",
        )
        self.heart = Heart.objects.create(user=self.user, review=self.review)

    def test_hearts_will_be_delete_when_the_review_deleted(self):
        self.review.delete()
        heart_count = Heart.objects.filter(review=self.review).count()

        self.assertEqual(0, heart_count)

    def test_hearts_will_be_delete_when_the_user_deleted(self):
        self.user.delete()
        heart_count = Heart.objects.filter(user=self.user).count()

        self.assertEqual(0, heart_count)


class ReviewCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()
        self.user = UserFactory().create()
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
        self.form = {
            "movieID": self.movie.id,
            "content": self.faker.text(),
            "rating": self.faker.random_int(1, 5),
        }

    def test_review_create_can_work(self):
        self.client.login(username=self.user.username, password="Passw0rd!")
        response = self.client.post(reverse("review:create"), self.form)

        self.assertEqual(1, Review.objects.filter(movie=self.movie).count())
        self.assertRedirects(
            response, expected_url=reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )


class ReviewDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory().create()
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
        self.review = Review.objects.create(
            user=self.user, movie=self.movie, content="test"
        )
        self.form = {"movieID": self.movie.id, "reviewID": self.review.id}

    def test_review_delete_can_work(self):
        response = self.client.post(
            reverse("review:delete", kwargs={"pk": self.review.pk}), self.form
        )

        self.assertEqual(0, Review.objects.filter(id=self.review.id).count())
        self.assertRedirects(
            response, expected_url=reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )


class ReviewEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory().create()
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
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            content="test",
        )
        self.form = {
            "movieID": self.movie.id,
            "reviewID": self.review.id,
            "content": "test edit",
            "rating": "1",
        }

    def test_revie_edit_can_work(self):
        response = self.client.post(
            reverse("review:edit", kwargs={"pk": self.review.pk}), self.form
        )

        self.assertEqual("test edit", Review.objects.get(id=self.review.id).content)
        self.assertEqual(1, Review.objects.get(id=self.review.id).rating)
        self.assertRedirects(
            response, expected_url=reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )


class HeartCreateTest(TestCase):
    def setUp(self):
        self.user = UserFactory().create()
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
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            content="test",
        )
        self.form = {
            "movieID": self.movie.id,
            "reviewID": self.review.id,
        }

    def test_heart_create_can_work(self):
        self.client.login(username=self.user.username, password="Passw0rd!")
        self.form["heart"] = ""
        response = self.client.post(
            reverse("review:heart", kwargs={"pk": self.review.pk}), self.form
        )

        self.assertEqual(
            1, Heart.objects.filter(user=self.user.id, review=self.review.id).count()
        )
        self.assertRedirects(
            response, expected_url=reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )

    def test_heart_delete_can_work(self):
        self.client.login(username=self.user.username, password="Passw0rd!")
        Heart.objects.create(user=self.user, review=self.review)

        response = self.client.post(
            reverse("review:heart", kwargs={"pk": self.review.pk}), self.form
        )

        self.assertEqual(
            0, Heart.objects.filter(user=self.user.id, review=self.review.id).count()
        )
        self.assertRedirects(
            response, expected_url=reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )
