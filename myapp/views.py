from django.shortcuts import render

# Create your views here.
def loginn(requset):
    return render(requset,'admin/login.html')