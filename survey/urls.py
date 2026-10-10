from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.SurveyListView.as_view(), name='list'),
    path('<int:pk>/', views.SurveyTakeView.as_view(), name='take'),
    path('<int:pk>/results/', views.SurveyResultView.as_view(), name='results'),
]