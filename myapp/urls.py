from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.loginn),
    path('addbatch/',views.addbatch),
    path('updatebatch/<id>',views.updatebatch),
    path('updatebatch_post/<id>',views.updatebatch_post),
    path('deletebatch/<id>',views.deletebatch),
    path('adminhome', views.adminhome),
    path('addtrainer', views.addtrainer),
    path('edittrainer/<id>',views.updatetraineradmin),
    path('edittrainer_post/<id>',views.updatetraineradmin_post),
    path('deletetrainer/<id>',views.deletetrainer),
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
    path('forgot_pass',views.forgot_pass),
    path('forgot_pass_post',views.forgot_pass_post),
    path('updateuser/<id>',views.updateuser),
    path('updateuser_post/<id>',views.updateuser_post),
    path('viewuserprofile',views.viewuserprofile),
]