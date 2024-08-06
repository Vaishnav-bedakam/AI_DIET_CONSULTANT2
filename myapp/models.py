from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    usertype=models.CharField(max_length=20)


class Trainer(models.Model):
    LOGIN=models.ForeignKey(Login,default=1,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    pin=models.CharField(max_length=20)
    post=models.CharField(max_length=20)
    age=models.CharField(max_length=3)
    sex=models.CharField(max_length=6)
    qualification = models.CharField(max_length=100)
    email=models.CharField(max_length=100, default="")
    mobilenumber = models.CharField(max_length=20, default="1234")
    experience = models.CharField(max_length=200)


class Batch(models.Model):
    Batch_title=models.CharField(max_length=20,default="")
    Batch_Capacity=models.CharField(max_length=20)
    Time_from=models.CharField(max_length=20)
    Time_to=models.CharField(max_length=20)

class User(models.Model):
    LOGIN = models.ForeignKey(Login, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    pin = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    age = models.CharField(max_length=6)
    sex = models.CharField(max_length=6)
    email=models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=20)
    occupation = models.CharField(max_length=20)



