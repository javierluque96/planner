from django.contrib import admin
from django.urls import path
from schedule import views

urlpatterns = [
    path('', views.schedule, name="Schedule"),
]