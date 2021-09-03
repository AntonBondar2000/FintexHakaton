from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import Home
urlpatterns = [
    path('home', Home.as_view(), name='home')
]

