from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_index, name='forum_index'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/create/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('thread/<int:thread_id>/message/', views.create_message, name='create_message'),
]
