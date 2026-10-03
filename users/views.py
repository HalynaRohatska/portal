from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView

from .forms import RegisterForm


class BaseView(TemplateView):
    template_name = "base.html"


class ProfileView(TemplateView):
    template_name = "task/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")

        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = "task/login.html"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class RegisterView(CreateView):
    template_name = "task/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect("home")
