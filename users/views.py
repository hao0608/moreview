from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView

from moreview import settings
from .forms import RegisterForm, ProfileUpdateForm, AdminCreateForm
from .models import User


# Create your views here.
class UserRegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save(commit=False)

        user.set_password(user.password)
        user.save()

        login(self.request, user)

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    http_method_names = ["post"]

    def get_redirect_url(self):
        return ""


class UserListView(UserPassesTestMixin, ListView):
    template_name = "user_list.html"
    model = User
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.is_superuser


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "profile.html"
    model = User
    login_url = reverse_lazy("users:login")

    def get(self, request, *args, **kwargs):
        if self.kwargs.get(self.pk_url_kwarg, "") == "":
            self.kwargs.update({"pk": request.user.pk})
        elif not request.user.is_superuser:
            return redirect(reverse_lazy("users:profile"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile-update-form"] = (
            ProfileUpdateForm(data=self.request.session.get("profile-update-form"))
            if self.request.session.get("profile-update-form")
            else ProfileUpdateForm(instance=self.object)
        )
        context["reset-password-form"] = (
            PasswordChangeForm(
                user=self.request.user,
                data=self.request.session.get("reset-password-form"),
            )
            if self.request.session.get("reset-password-form")
            else PasswordChangeForm(user=self.request.user)
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("users:profile")
    login_url = reverse_lazy("users:login")

    def get(self, request, *args, **kwargs):
        return redirect(reverse("users:profile"))

    def post(self, request, *args, **kwargs):
        self.kwargs.update({"pk": request.user.pk})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["profile-update-form"] = None
        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session["profile-update-form"] = form.data
        return redirect(reverse("users:profile"))


class AdminCreateView(UserPassesTestMixin, CreateView):
    template_name_suffix = "_create_form"
    model = User
    form_class = AdminCreateForm
    success_url = reverse_lazy("users:list")
    login_url = reverse_lazy("users:login")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        form.instance.is_superuser = True
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UpdateView):
    model = User
    fields = []
    success_url = reverse_lazy("movie:list")
    login_url = reverse_lazy("users:login")

    def get(self, request, *args, **kwargs):
        return redirect(reverse("users:profile"))

    def post(self, request, *args, **kwargs):
        self.kwargs.update({"pk": request.user.pk})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_active = False
        logout(self.request)
        return super().form_valid(form)


class UserResetPasswordView(PasswordChangeView):
    success_url = reverse_lazy("users:profile")

    def get(self, request, *args, **kwargs):
        return redirect(reverse("users:profile"))

    def post(self, request, *args, **kwargs):
        self.kwargs.update({"pk": request.user.pk})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session["reset-password-form"] = None
        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session["reset-password-form"] = form.data
        return redirect(f"{reverse('users:profile')}#reset-password")
