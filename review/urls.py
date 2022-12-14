from django.urls import path


from . import views

app_name = "review"
urlpatterns = [
    path("reviews/create", views.ReviewCreateView.as_view(), name="create"),
    path("reviews/<int:pk>/edit", views.ReviewEditView.as_view(), name="edit"),
    path("reviews/<int:pk>/delete", views.ReviewDeleteView.as_view(), name="delete"),
    path("reviews/<int:pk>/heart", views.HeartView.as_view(), name="heart"),
]
