# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# import demjson
# from django.db.models import Q
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, redirect
# import datetime
# import random
# from matplotlib.backends.backend_agg import FigureCanvasAgg

# import matplotlib.pyplot as plt
# # Create your views here.
# from myapp.models import *


# #admin side
# def loginn(request):
#     return render(request,'admin/login.html')
# def register(request):
#     return render(request, "user/register.html")
# views.py

from django.shortcuts import render

def loginn(request):
    return render(request, 'admin/login.html')
def register(request):
    return render(request, "user/register.html")
