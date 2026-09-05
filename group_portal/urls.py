"""
URL configuration for group_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls", namespace="core")),                      #  головна сторінка
    path("users", include("users.urls", namespace="users")),               #  автентифікація, профілі
    path("diary/", include("diary.urls", namespace="diary")),              #  електронний щоденник
    path("forum/", include("forum.urls", namespace="forum")),              #  форум
    path("events/", include("event_calendar.urls", namespace="events")),   #  події та календар
    path("annonc/", include("announcement.urls", namespace="annonc")),     #  оголошення
    path("survey/", include("survey.urls", namespace="survey")),           #  опитування
]
