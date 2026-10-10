from django.urls import path
from .views import BaseView, ProfileView, CustomLoginView, CustomLogoutView, RegisterView

app_name = "users"

urlpatterns = [
    path("base/", BaseView.as_view(), name="base"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
