from django.urls import reverse
from django.shortcuts import render
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.http import HttpResponseRedirect,HttpResponse
from users.models import User
from review.models import Review
from .models import Report
from .forms import ReportModelForm

# Create your views here.
class ReportListView(ListView):
    model = Report
    report_template_name="report_list.html"
    report_manage_template_name="report_review_form.html"
    
    def get_template_names(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return [self.report_manage_template_name]
        else:
            return [self.report_template_name]

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)

        if self.request.user.is_superuser:
            query= self.request.GET.get('q')
            status=self.request.GET.get('status')

            if query is not None and status != "all":
                report_obj=Report.objects.filter(
                    review__movie__name__contains=query,
                    status=status
                ).order_by("-date_updated")
            else:
                report_obj=Report.objects.all().order_by("-date_updated")
            
            context["status"] = status
            context["object_list"]=report_obj
        else:
            context["object_list"]=Report.objects.filter(
                user=self.request.user
            ).exclude(status=3).order_by("-date_updated")
        return context

class ReportCreatetView(View):
    def post(self, request, *args, **kwargs):
        user=User.objects.get(id=self.request.user.id)
        review=Review.objects.get(id=request.POST['reviewID'])
        content=request.POST['content']
        report=Report.objects.create(
            user=user,
            review=review,
            content=content,
        )
        return HttpResponseRedirect(reverse("movie:detail",kwargs={"pk":review.movie.pk}))

class ReportDeleteView(View):
    def post(self, request, *args, **kwargs):
        report=Report.objects.filter(id=self.kwargs['pk'])
        report.update(status=3)
        return HttpResponseRedirect(reverse("reports:list"))

class ReportReviewView(View):
    def post(self, request, *args, **kwargs):
        report=Report.objects.filter(id=self.kwargs['pk'])
        print(request.POST.keys())
        if "accept_report" in request.POST.keys():
            report.update(status=1,handler=self.request.user)
        elif "refuse_report" in request.POST.keys():
            report.update(status=2,handler=self.request.user)
        
        return HttpResponseRedirect(reverse("reports:list"))
