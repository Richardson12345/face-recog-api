from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.home, name="recog-home"),
    path('about/', views.about, name="recog-about"),
    path('recog/', views.RecogList.as_view()),
    path('insert/', views.CreateList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)