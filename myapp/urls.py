from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.loginn),
    #  path('adminhome', views.adminhome),
     path('register',views.register),
]