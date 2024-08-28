from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Login, User, Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.db.models import Q
from myapp.models import *

import datetime
import random
import demjson

def loginn(request):
    return render(request, 'admin/login.html')
def addbatch(request):
    return render(request, 'admin/Add Batch.html')
def addtrainer(request):
    return render(request, 'admin/Add Trainer.html')
def viewbatch(request):
    res = Batch.objects.all()
    if res.exists():
        l=[]
        for i in res:
            a=i.Batch_Capacity
            re = assign.objects.filter(REQUEST__BATCH_id=i.id,
                                       REQUEST__status="approved").count()

            b=int(a)-int(re)
            l.append({
                "re":re,
                "Batch_title":i.Batch_title,
                "Batch_Capacity":i.Batch_Capacity,
                "Time_from":i.Time_from,
                "Time_to":i.Time_to,
                "c":b,
                "id":i.id,

            })


        return render(request, 'admin/View Batch.html',{'data':l})
    else:
        return render(request,'admin/nobatches.html')


def viewtrainer(request):
    res=Trainer.objects.all()
    if res.exists():
        return render(request, 'admin/View Trainer.html',{'data':res})
    else:
        return render(request,'admin/notrainer.html')


def adminhome(request):
    res = Request.objects.filter(status="pending")
    if res.exists():
        lst = ["New user request in " + i.BATCH.Batch_title for i in res]
        return render(request, 'index.html', {'lst': lst})
    else:
        return render(request, 'index.html')

def login_post(request):
    usernam = request.POST.get('textfield')
    passwor = request.POST.get('textfield2')
    r = Login.objects.filter(username=usernam, password=passwor)
    if r.exists():
        r = r.first()
        if r.usertype == "admin":
            return redirect('/adminhome')
        elif r.usertype == "trainer":
            request.session['lid'] = r.id
            return redirect('/trainerhome')
        elif r.usertype == "user":
            request.session['lid'] = r.id
            return redirect('/userhome')
        else:
            return HttpResponse("<script>alert('Invalid username or password');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Invalid username or password');window.location='/'</script>")
def addbatch_post(request):
    batchtitle=request.POST['textfield5']
    batchcapacity=request.POST['textfield']
    from1=request.POST['textfield2']
    to=request.POST['textfield3']
    r = Batch.objects.filter(Batch_title=batchtitle,Batch_Capacity=batchcapacity,Time_from=from1,Time_to=to)
    r1= Batch.objects.filter(Batch_title=batchtitle)
    if r1.exists():
        if r.exists():
             return HttpResponse("<script>alert('Already Exist');window.location='addbatch/'</script>")
        return HttpResponse("<script>alert('Batch name exists');window.location='addbatch/'</script>")
    else:
        obj=Batch()
        obj.Batch_Capacity=batchcapacity
        obj.Time_from=from1
        obj.Time_to=to
        obj.Batch_title=batchtitle
        obj.save()
        return HttpResponse('<script>alert("Added");window.location="/viewbatch#abc"</script>')


def addtrainer_post(request):
    name1=request.POST['textfield']
    place1=request.POST['textfield2']
    pin1=request.POST['textfield3']
    post1=request.POST['textfield4']
    age1=request.POST['textfield5']
    gender1=request.POST['RadioGroup1']
    qualification1=request.POST['textarea']
    experience1=request.POST['textarea2']
    mnumber1=request.POST['textfield6']
    email1=request.POST['textfield7']
    p=random.randint(0000,9999)
    r = Trainer.objects.filter(name=name1,place=place1,pin=pin1,post=post1,age=age1,sex=gender1,qualification=qualification1,experience=experience1,
                               mobilenumber=mnumber1,email=email1)
    r1=Login.objects.filter(username=email1)
    import smtplib

    #dietconsultant2024@gmail.com
    #rkdjjzbccfsaonne

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("nutrifit20241@gmail.com", "yuxxqtudpztjkzbl")
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = "nutrifit20241@gmail.com"
    msg['To'] = email1
    msg['Subject'] = "Your Password for Nutrifit"
    body = "Username : " + str(email1)+ "\nPassword : "+str(p)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    if r.exists():
        if r1.exists():
            return HttpResponse("<script>alert('Email Already Exists');window.location='addtrainer#abc'</script>")

        return HttpResponse("<script>alert('Trainer Already Exists');window.location='addtrainer#abc'</script>")

    else:
        obj2=Login()
        obj2.username=email1
        obj2.password=p
        obj2.usertype='trainer'
        obj2.save()
        obj=Trainer()
        obj.name=name1
        obj.place=place1
        obj.pin=pin1
        obj.post = post1
        obj.age=age1
        obj.sex = gender1
        obj.qualification = qualification1
        obj.experience = experience1
        obj.mobilenumber = mnumber1
        obj.email = email1
        obj.LOGIN=obj2
        obj.save()

        return HttpResponse("<script>alert('added');window.location='viewtrainer#abc'</script>")
#trainer
def viewprofile(request):
    res=Trainer.objects.get(LOGIN=request.session['lid'])
    return render(request,'trainer/view profile.html',{'data':res})
def trainerhome(request):
    return render(request,'trainerIndex.html')

def register(request):
    return render(request, "user/register.html")
def forgot_pass(request):
    return render(request, "forget_password.html")

def forgot_pass_post(request):
    email=request.POST['textfield']
    log_obj=Login.objects.filter(username=email)
    if log_obj.exists():
        res=log_obj[0]
        import smtplib

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("nutrifit20241@gmail.com", "yuxxqtudpztjkzbl")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "nutrifit20241@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for NUTRIFIT"
        body = " Your password is : " + str(res.password)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        return HttpResponse("<script>alert('Password sent to mail');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Username not found');window.location='/'</script>")
#user
def register_post(request):
    name1 = request.POST.get('textfield')
    place1 = request.POST.get('textfield2')
    pin1 = request.POST.get('textfield3')
    post1 = request.POST.get('textfield4')
    age1 = request.POST.get('textfield5')
    gender1 = request.POST.get('RadioGroup1')
    occupation1 = request.POST.get('textfield8')
    password1 = request.POST.get('textfield9')
    cpassword = request.POST.get('textfield10')
    mnumber1 = request.POST.get('textfield6')
    email1 = request.POST.get('textfield7')

    if password1 != cpassword:
        return HttpResponse("<script>alert('Passwords do not match');window.location='register'</script>")

    if User.objects.filter(email=email1).exists() or Login.objects.filter(username=email1).exists():
        return HttpResponse("<script>alert('Email Already Exists');window.location='register'</script>")

    login_obj = Login(username=email1, password=password1, usertype='user')
    login_obj.save()

    user_obj = User(
        name=name1,
        place=place1,
        pin=pin1,
        post=post1,
        age=age1,
        sex=gender1,
        occupation=occupation1,
        mobilenumber=mnumber1,
        email=email1,
        LOGIN=login_obj
    )
    user_obj.save()

    return HttpResponse("<script>alert('Registered Successfully');window.location='/'</script>")

def userhome(request):
    return render(request, 'userIndex.html')
