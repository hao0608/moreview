from django.urls import path


from . import views

app_name = "reports"
urlpatterns = [
    path("reports/create", views.ReportCreatetView.as_view(), name="create"),
    path("reports/<int:pk>/delete", views.ReportDeleteView.as_view(), name="delete"),
    path("reports/<int:pk>/edit", views.ReportReviewView.as_view(), name="edit"),
    path("reports", views.ReportListView.as_view(), name="list"),
]
