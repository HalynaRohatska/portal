from django.contrib import admin
from django.urls import path, include
from users.views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('diary/', include('diary.urls', namespace='diary')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('events/', include('event_calendar.urls', namespace='events')),
    path('annonc/', include('announcement.urls', namespace='annonc')),
    path('survey/', include('survey.urls', namespace='survey')),
]
