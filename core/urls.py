from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import Home
urlpatterns = [
    path('user/<int:id>', Home.as_view(), name='home')
]

