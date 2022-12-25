from django.db import models
from users.models import User
from review.models import Review
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.
class Report(models.Model):
    UNDERPROCESS = 0
    SUCCESS = 1
    FAILED = 2
    TAKEBACK = 3
    REPORT_STATUS = [
        (UNDERPROCESS, "待處理"),
        (SUCCESS, "檢舉成功"),
        (FAILED, "檢舉失敗"),
        (TAKEBACK, "已撤回"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("user"))
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name=_("review")
    )
    handler = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name=_("admin")
    )
    content = models.TextField(blank=False, null=False, max_length=500)
    status = models.IntegerField(default=UNDERPROCESS, choices=REPORT_STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("movie:detail", kwargs={"pk": self.pk})
