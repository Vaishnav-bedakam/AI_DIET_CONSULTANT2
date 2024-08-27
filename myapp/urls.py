from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.loginn),
    path('addbatch/',views.addbatch),
    path('adminhome', views.adminhome),
    path('addtrainer', views.addtrainer),
    path('login_post', views.login_post),
    path('viewtrainer',views.viewtrainer),
    path('viewbatch', views.viewbatch),
    path('addbatch_post', views.addbatch_post),
    path('addtrainer_post', views.addtrainer_post),
    path('viewprofile/',views.viewprofile),
     path('trainerhome/',views.trainerhome),
    path('register',views.register),
    path('register_post',views.register_post),
    path('userhome/',views.userhome),
]