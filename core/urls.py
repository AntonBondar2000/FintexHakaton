from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import Home
from django.views.generic.base import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url='user/1', permanent=False), name='index'),
    path('user/<int:id>', Home.as_view(), name='home')
]

