from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.loginn),
    path('adminhome', views.adminhome),
    path('login_post', views.login_post),
    path('register',views.register),
    path('register_post',views.register_post),
    path('userhome/',views.userhome),
]