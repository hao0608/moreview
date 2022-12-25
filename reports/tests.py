from django.test import TestCase, Client
from django.urls import reverse
import time

from faker import Faker
from movie.models import Movie, Tag
from review.models import Review, Heart
from reports.models import Report
from reports.views import *
from users.factories import UserFactory

# Create your tests here.
class ReportModelTest(TestCase):
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
        self.report = Report.objects.create(
            user=self.user, review=self.review, content="report test"
        )

    def test_data_updated_field_updates_when_record_updates(self):
        self.report.content = self.faker.text()
        time.sleep(1)
        self.report.save()

        self.assertNotEqual(
            self.report.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            self.report.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def test_reports_will_be_deleted_when_the_movie_deleted(self):
        self.movie.delete()
        report_count = Report.objects.filter(id=self.report.id).count()

        self.assertEqual(0, report_count)

    def test_reports_will_be_deleted_when_the_review_deleted(self):
        self.review.delete()
        report_count = Report.objects.filter(id=self.report.id).count()

        self.assertEqual(0, report_count)

    def test_reports_will_be_deleted_when_the_user_deleted(self):
        self.user.delete()
        report_count = Report.objects.filter(id=self.report.id).count()

        self.assertEqual(0, report_count)


class ReportCreateTest(TestCase):
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
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            content="test",
        )
        self.form = {
            "reviewID": self.review.id,
            "content": self.faker.text(),
        }

    def test_review_create_can_work(self):
        self.client.login(username=self.user.username, password="Passw0rd!")
        response = self.client.post(reverse("reports:create"), self.form)

        self.assertEqual(1, Report.objects.filter(review=self.review).count())
        self.assertRedirects(
            response, expected_url=reverse("movie:detail", kwargs={"pk": self.movie.pk})
        )


class ReportDeleteTest(TestCase):
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
        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            content="test",
        )
        self.report = Report.objects.create(
            user=self.user, review=self.review, content="report test"
        )

    def test_report_delete_can_work(self):
        self.client.login(username=self.user.username, password="Passw0rd!")
        response = self.client.post(
            reverse("reports:delete", kwargs={"pk": self.report.id})
        )
        updated_report = Report.objects.get(id=self.report.id)
        self.assertRedirects(response, expected_url=reverse("reports:list"))
        self.assertEqual(3, updated_report.status)


class ReportListViewTest(TestCase):
    def setUp(self):
        self.view = ReportListView
        self.user = UserFactory().create()
        self.client = Client()

    def test_report_lsit_template_is_correct(self):
        self.assertEqual("report_list.html", self.view.report_template_name)

    def test_report_manage_template_is_correct(self):
        self.assertEqual(
            "report_review_form.html", self.view.report_manage_template_name
        )

    def test_report_list_page_can_render(self):
        self.client.login(username=self.user.username, password="Passw0rd!")
        response = self.client.get(reverse("reports:list"))

        self.assertEqual(200, response.status_code)


class ReportReviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()
        self.user = UserFactory().create()
        self.admin = UserFactory().is_superuser().create()
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
        self.report = Report.objects.create(
            user=self.user, review=self.review, content="report test"
        )

    def test_accept_report_can_work(self):
        self.client.login(username=self.admin.username, password="Passw0rd!")
        response = self.client.post(
            reverse("reports:edit", kwargs={"pk": self.report.id}),
            {"accept_report": ""},
        )
        updated_report = Report.objects.get(id=self.report.id)

        self.assertEqual(1, updated_report.status)
        self.assertEqual(self.admin.username, updated_report.handler.username)

    def test_accept_report_can_work(self):
        self.client.login(username=self.admin.username, password="Passw0rd!")
        response = self.client.post(
            reverse("reports:edit", kwargs={"pk": self.report.id}),
            {"refuse_report": ""},
        )
        updated_report = Report.objects.get(id=self.report.id)

        self.assertEqual(2, updated_report.status)
        self.assertEqual(self.admin.username, updated_report.handler.username)
