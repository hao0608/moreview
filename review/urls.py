from django.urls import path


from . import views

app_name = "review"
urlpatterns = [
    path("reviews/create", views.ReviewCreateView.as_view(), name="create"),
]
