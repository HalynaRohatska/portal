from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "annonc"

urlpatterns = [
    path("", views.AnnouncementListView.as_view(), name="list"),
    path("<int:pk>/", views.AnnouncementDetailView.as_view(), name="detail"),
    path("create/", views.AnnouncementCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.AnnouncementUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AnnouncementDeleteView.as_view(), name="delete"),
]



