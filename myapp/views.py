from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import demjson
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import datetime
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg

import matplotlib.pyplot as plt
# Create your views here.
from myapp.models import *


#admin side
def loginn(request):
    return render(request,'admin/login.html')

def addbatch(request):
    return render(request, 'admin/Add Batch.html')

def addtrainer(request):
    return render(request, 'admin/Add Trainer.html')

def assigntrainer(request,id):
    res=Trainer.objects.all()
    return render(request, 'admin/Assign Trainer.html',{'data':res,'id': id})

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
def viewfeedback(request):
    res=feedback.objects.all()
    if res.exists():
        return render(request, 'admin/view feedback.html',{'data':res})
    else:
        return render(request,'admin/nofeedback.html')

def viewrequest(request,id):
    res = Request.objects.filter(BATCH=Batch.objects.get(id=id),status="pending")
    if res.exists():
        return render(request, 'admin/View Request.html',{'data':res})
    else:
        return render(request,'admin/norequest.html')

def viewtrainer(request):
    res=Trainer.objects.all()
    if res.exists():
        return render(request, 'admin/View Trainer.html',{'data':res})
    else:
        return render(request,'admin/notrainer.html')

def adminhome(request):
    res=Request.objects.filter(status="pending")
    if res.exists():
        lst=[]
        for i in res:
            bat=i.BATCH.Batch_title
            lst.append("New user request in " + bat)
        return render(request, 'index.html', {'lst':lst})
    else:
        return render(request, 'index.html')

def login_post(request):
     usernam=request.POST['textfield']
     passwor = request.POST['textfield2']
     r=Login.objects.filter(username=usernam,password=passwor)
     if r.exists():
         r=r[0]
         if r.usertype=="admin":
             return redirect('/adminhome')
         elif r.usertype=="trainer":
             request.session['lid']=r.id
             return redirect('/trainerhome')
         elif r.usertype=="user":
             request.session['lid']=r.id
             return redirect('/userhome')
         else:
             return HttpResponse("<script>alert('Invalid username or password');window.location='/'</script>")
     else:
         return HttpResponse("<script>alert('Invalid username or password');window.location='/'</script>")


def viewbatchinfo(request):
    res=Batch.objects.all()
    return render(request,'admin/view batch info.html',{'data':res})


def viewbatchtrainer(request,id):
    request.session['bid']=id
    a=Request.objects.filter(BATCH=Batch.objects.get(id=id),status="approved")
    data=[]
    tid=[]
    if a.exists():
        for i in a:
            res=assign.objects.get(REQUEST=i)

            if res.TRAINER.id not in tid:
                r=assign.objects.filter(REQUEST__BATCH_id=id, TRAINER=Trainer.objects.get(id=res.TRAINER.id)).count()

                tid.append(res.TRAINER.id)
                data.append({'d' : res, 'r' : r})
        return render(request,'admin/view batch trainer.html',{'data':data})
    else:
        return render(request,'admin/nobatchtrainer.html')

def viewbatchmember(request,id):
    bid=request.session['bid']
    tid = Trainer.objects.get(id=id)
    re = assign.objects.filter(TRAINER=tid)
    if re.exists():
        l=[]
        for i in re:

            res = Request.objects.filter(id=i.REQUEST.id,BATCH=bid)
            for ij in res:
                l.append({
                    "name":ij.USER.name,
                    "sex":ij.USER.sex,
                    "age":ij.USER.age,
                    "time":ij.time,
                    "id": ij.USER.id,
                    "bid":bid,
                })
        return render(request, 'admin/view batch members.html',{'data':l,'bid':bid})
    else:
        return render(request,'admin/nobatchmember.html')
def assignbatch_post(request,id):

    tnr=request.POST['select']
    r=Request.objects.get(id=id)
    res=assign.objects.filter(REQUEST=r)
    if res.exists():
        return HttpResponse("<script>alert('already added');window.location='/viewbatch#abc'</script>")

    else:
        d = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        obj=assign()
        obj.REQUEST=Request.objects.get(id=id)
        obj.TRAINER=Trainer.objects.get(id=tnr)
        obj.time=d
        obj.save()
        Request.objects.filter(id=id).update(status='approved')

        return HttpResponse("<script>alert('added');window.location='/viewbatch#abc'</script>")



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

def updatebatch(request,id):
    res=Batch.objects.get(id=id)
    return render(request,'admin/update Batch.html',{'data':res,'id':id})

def updatebatch_post(request,id):
    batchcapacity=request.POST['textfield']
    from1=request.POST['textfield2']
    to=request.POST['textfield3']
    batchtitle=request.POST['textfield5']
    Batch.objects.filter(id=id).update(Batch_title=batchtitle,Batch_Capacity=batchcapacity,Time_from=from1,Time_to=to)
    return HttpResponse("<script>alert('added');window.location='/viewbatch#abc'</script>")

def deletebatch(request,id):
    Batch.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Deleted');window.location='/viewbatch#abc'</script>")

def updatetrainer(request,id):
    res=Trainer.objects.get(id=id)
    return render(request,'admin/update Trainer.html',{'data':res,'id':id})

def updatetraineradmin(request,id):
    res=Trainer.objects.get(id=id)
    return render(request,'admin/edit Trainer.html',{'data':res,'id':id})

def updatetrainer_post(request,id):
    name1 = request.POST['textfield']
    place1 = request.POST['textfield2']
    pin1 = request.POST['textfield3']
    post1 = request.POST['textfield4']
    age1 = request.POST['textfield5']
    gender1 = request.POST['RadioGroup1']
    qualification1 = request.POST['textarea']
    experience1 = request.POST['textarea2']
    mnumber1 = request.POST['textfield6']
    email1 = request.POST['textfield7']
    Trainer.objects.filter(id=id).update(name=name1,place=place1,pin=pin1,post=post1,age=age1,sex=gender1,qualification=qualification1,experience=experience1,mobilenumber=mnumber1,email=email1)
    return HttpResponse("<script>alert('added');window.location='/viewprofile/#abc'</script>")

def updatetraineradmin_post(request,id):
    name1 = request.POST['textfield']
    place1 = request.POST['textfield2']
    pin1 = request.POST['textfield3']
    post1 = request.POST['textfield4']
    age1 = request.POST['textfield5']
    gender1 = request.POST['RadioGroup1']
    qualification1 = request.POST['textarea']
    experience1 = request.POST['textarea2']
    mnumber1 = request.POST['textfield6']
    email1 = request.POST['textfield7']
    Trainer.objects.filter(id=id).update(name=name1,place=place1,pin=pin1,post=post1,age=age1,sex=gender1,qualification=qualification1,experience=experience1,mobilenumber=mnumber1,email=email1)
    return HttpResponse("<script>alert('added');window.location='/viewtrainer#abc'</script>")

def deletetrainer(request,id):
    trainer_instance = Trainer.objects.get(id=id)

    login_instance = trainer_instance.LOGIN

    trainer_instance.delete()
    login_instance.delete()

    return HttpResponse("<script>alert('Trainer and associated Login deleted');window.location='/viewtrainer#abc'</script>")

def rejectrequest(request,id):
    return render(request,"admin/send reason.html",{"id":id})


def deleterequest(request,id):
    reason=request.POST['textarea']
    Request.objects.filter(id=id).update(status='rejected   '+reason)

    return HttpResponse("<script>alert('rejected!');window.location='/viewbatch#abc'</script>")

#trainer
def uploaddietplan(request,id, uid):
    health.objects.filter(id=id)
    return render(request,'trainer/Upload Diet Plan.html',{'id':id, 'uid':uid})

def uploaddietplan_post(request,id, uid):
    title1=request.POST['time']
    description1=request.POST['description']
    d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    r = Trainer.objects.get(LOGIN=request.session['lid'])
    obj = diet()
    obj.date = d1
    obj.title=title1
    obj.description=description1
    obj.TRAINER=r
    obj.USER_id=uid
    obj.save()
    return HttpResponse("<script>alert('Added');window.location.href='/uploaddietplan/{}/{}';</script>".format(id,uid))



def viewdietplan(request,uid):
    res=diet.objects.filter(USER_id=uid)
    if res.exists():
        return render(request,'trainer/viewdietplan.html',{'data':res})
    else:
        return render(request,'trainer/nodietplan.html')


def editdietplan(request,id):
    res = diet.objects.get(id=id)

    return render(request, 'trainer/edit Diet Plan.html', {'data': res, 'id': id})

def editdietplan_post(request,id):
    title1=request.POST['time']
    description1=request.POST['description']
    d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    diet.objects.filter(id=id).update(title=title1, description=description1, date=d1)
    return HttpResponse("<script>alert('Edited Successfully');window.location='/trainerhome'</script>")

def deletedietplan(request,id):
    diet.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Edited Successfully');window.location='/trainerhome'</script>")
def addtips(request, uid):
    return render(request,'trainer/add tips.html', {'uid':uid})

def addworkout(request,uid):
    return render(request,'trainer/add workout.html',{'uid':uid})
def viewtips(request,uid):
    r = Trainer.objects.get(LOGIN=request.session['lid'])
    res = tips.objects.filter(TRAINER=r, USER_id=uid)
    if res.exists():
        return render(request,'trainer/view tips.html',{'data':res})
    else:
        return render(request,'trainer/notips.html')


def viewworkout(request,uid):
    r = Trainer.objects.get(LOGIN=request.session['lid'])
    res = workout.objects.filter(TRAINER=r,USER_id=uid)
    if res.exists():
        return render(request,'trainer/view workout.html',{'data':res})
    else:
        return render(request,'trainer/noworkout.html')
def addtips_post(request,uid):
    title=request.POST['textfield']
    description=request.POST['textarea']
    d = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    r = Trainer.objects.get(LOGIN=request.session['lid'])
    obj=tips()
    obj.title=title
    obj.description=description
    obj.date=d
    obj.TRAINER=r
    obj.USER_id=uid

    obj.save()

    return HttpResponse("<script>alert('Added');window.location.href='/viewtips/{}#abc';</script>".format(uid))


def addworkout_post(request,uid):
    title=request.POST['textfield']
    description=request.POST['textarea']
    video=request.FILES['fileField']
    d = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
    d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    r = Trainer.objects.get(LOGIN=request.session['lid'])
    fs=FileSystemStorage()
    fs.save(r"E:\nutrifit\AI_DIET_CONSULTANT\myapp\static\videos\\" + d +".mp4", video)

    path="/static/videos/" + d + ".mp4"
    r1 = workout.objects.filter(title=title,description=description)
    if r1.exists():
        return HttpResponse("<script>alert('Added');window.location.href='/viewworkout/{}#abc';</script>".format(uid))
    else:
        obj=workout()
        obj.title=title
        obj.description=description
        obj.date=d1
        obj.video=path
        obj.TRAINER=r
        obj.USER_id=uid
        obj.save()
        return HttpResponse("<script>alert('Added');window.location.href='/viewworkout/{}#abc';</script>".format(uid))

def edittip(request,id):
    res = tips.objects.get(id=id)
    return render(request, 'trainer/edit tip.html', {'data': res, 'id': id})

def edittip_post(request,id):
    title = request.POST['textfield']
    description = request.POST['textarea']
    d = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    tips.objects.filter(id=id).update(title=title,description=description,date=d)
    return HttpResponse("<script>alert('edited');window.location='/trainerhome'</script>")

def deletetip(request,id):
    tips.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('deleted');window.location='/trainerhome'</script>")

def editworkout(request,id):
    res = workout.objects.get(id=id)
    return render(request, 'trainer/editworkout.html', {'data': res, 'id': id})

# def editworkout_post(request,id):
#     title=request.POST['textfield']
#     description=request.POST['textarea']
#     video=request.FILES['fileField']
#     d = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
#     d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
#     fs=FileSystemStorage()
#     fs.save(r"E:\nutrifit\AI_DIET_CONSULTANT\myapp\static\videos\\" + d +".mp4", video)

#     path="/static/videos/" + d + ".mp4"
#     workout.objects.filter(id=id).update(title=title, description=description, video=path,date=d1)
#     return HttpResponse("<script>alert('edited');window.location='/trainerhome'</script>")
def editworkout_post(request, id):
    title = request.POST.get('textfield')
    description = request.POST.get('textarea')
    video = request.FILES.get('fileField', None)  # Use .get() to avoid the KeyError

    if video:  # Proceed only if a video is uploaded
        d = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
        d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        fs = FileSystemStorage()
        fs.save(r"E:\nutrifit\AI_DIET_CONSULTANT\myapp\static\videos\\" + d + ".mp4", video)
        path = "/static/videos/" + d + ".mp4"
        workout.objects.filter(id=id).update(title=title, description=description, video=path, date=d1)
    else:
        workout.objects.filter(id=id).update(title=title, description=description)
    
    return HttpResponse("<script>alert('edited');window.location='/trainerhome'</script>")


def deleteworkout(request,id):
    workout.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('deleted');window.location='/trainerhome'</script>;")
def viewprofile(request):
    res=Trainer.objects.get(LOGIN=request.session['lid'])
    return render(request,'trainer/view profile.html',{'data':res})
def trainerhome(request):
    return render(request,'trainerIndex.html')
def viewassignedbatch(request):
    r = Trainer.objects.get(LOGIN=request.session['lid'])
    res = assign.objects.filter(TRAINER=r, REQUEST__status="approved")
    if res.exists():
        L = []
        seen_batch_ids = set()

        for i in res:
            re = Request.objects.filter(id=i.REQUEST.id).order_by('BATCH').values()
            rr = Request.objects.filter(BATCH=i.REQUEST.BATCH.id, status="approved").count()
            r1 = assign.objects.filter(REQUEST__BATCH_id=i.REQUEST.BATCH.id, TRAINER=r, REQUEST__status="approved").count()

            for ij in re:
                batch_id = i.REQUEST.BATCH.id

                if batch_id not in seen_batch_ids:
                    a = i.REQUEST.BATCH.Batch_Capacity
                    L.append({
                        "title": i.REQUEST.BATCH.Batch_title,
                        "Batch_Capacity": i.REQUEST.BATCH.Batch_Capacity,
                        "Time_from": i.REQUEST.BATCH.Time_from,
                        "Time_to": i.REQUEST.BATCH.Time_to,
                        "id": batch_id,
                        "rr": rr,
                        "r1": r1,
                        "c": int(a) - int(rr),
                    })
                    seen_batch_ids.add(batch_id)

        return render(request, 'trainer/view assigned batch.html', {'data': L})
    else:
        return render(request,'trainer/nobatches.html')

def viewmembers(request,id):
    tid = Trainer.objects.get(LOGIN=request.session['lid'])
    l=[]

    re = assign.objects.filter(TRAINER=tid, REQUEST__status="approved")
    if re.exists():
        for i in re:
            res = Request.objects.filter(BATCH=id, id=i.REQUEST.id)
            for ij in res:
                l.append({
                    "name":ij.USER.name,
                    "place":ij.USER.place,
                    "age":ij.USER.age,
                    "sex":ij.USER.sex,
                    "occupation":ij.USER.occupation,
                    "mobilenumber":ij.USER.mobilenumber,
                    "email":ij.USER.email,
                    "id":ij.USER.id
                })

        return render(request,'trainer/view members.html',{'data':l})
    else:
        return render(request,'trainer/nomembers.html')
def viewhealthinfo(request, id):
    try:
        user = User.objects.get(id=id)
        request_obj = Request.objects.filter(USER=user).latest('id')  # Assuming the latest request contains the batch information
        batch_id = request_obj.BATCH.id
        health_records = health.objects.filter(USER=user).order_by('-id')
        return render(request, 'trainer/view health info.html', {'data': health_records, 'uid': id, 'batch_id': batch_id})
    except (User.DoesNotExist, Request.DoesNotExist):
        return render(request, 'trainer/nohealth.html')

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
def register(request):
    return render(request, "user/register.html")
    
def viewuserprofile(request):
    res = User.objects.get(LOGIN=request.session['lid'])
    return render(request,"user/viewprofile.html",{"data":res})

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
def updateuser(request,id):
    res=User.objects.get(id=id)
    res1 = Login.objects.get(id=id)
    return render(request,'user/updateprofile.html',{'data':res,'id':id,'data1':res1})

def updateuser_post(request,id):
    name1 = request.POST['textfield']
    place1 = request.POST['textfield2']
    pin1 = request.POST['textfield3']
    post1 = request.POST['textfield4']
    age1 = request.POST['textfield5']
    gender1 = request.POST['RadioGroup1']
    occupation1 = request.POST['textfield8']
    password1 = request.POST['textfield9']
    mnumber1 = request.POST['textfield6']
    email1 = request.POST['textfield7']
    User.objects.filter(id=id).update(name=name1, place=place1, pin=pin1, post=post1, age=age1, sex=gender1,
                                         occupation=occupation1,mobilenumber=mnumber1,email=email1)
    Login.objects.filter(id=request.session['lid']).update(password=password1)
    return HttpResponse("<script>alert('Updated Successfully');window.location='/viewuserprofile'</script>")
def sendfeedback(request):
    return render(request, 'user/send feedback.html')

def sendfeedback_post(request):
    feedbackk=request.POST['textarea']
    d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    r = feedback.objects.filter(time=d1)
    if r.exists():
        return HttpResponse("alert('already submitted');window.location='sendfeedback/#abc'")
    else:
        obj=feedback()
        obj.feedback=feedbackk
        obj.time=d1
        obj.USER=User.objects.get(LOGIN=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('Successfully Sent');window.location='/userhome'</script>")
def viewbatchuser(request):

    batches = Batch.objects.all()

    if batches.exists():


        batch_list = []
        request_list = []




        for batch in batches:

            assignment_count = assign.objects.filter(REQUEST__BATCH=batch.id).count()


            capacity_remaining = int(batch.Batch_Capacity) - int(assignment_count)


            batch_list.append({
                "id": batch.id,
                "Batch_title": batch.Batch_title,
                "Batch_Capacity": batch.Batch_Capacity,
                "Time_from": batch.Time_from,
                "Time_to": batch.Time_to,
                "Capacity_remaining": capacity_remaining,
                "assignment_count": assignment_count,
            })

        user_requests2 = Request.objects.filter(USER__LOGIN__id=request.session['lid']).order_by('-id')


        if user_requests2.exists():
            user_requests2 = user_requests2[0]

            request_list.append({
                "status": user_requests2.status,
            })
        else:

            request_list.append({})


        return render(request, 'user/view batch.html', {'data': batch_list, 'data1': request_list})
    else:
        return render(request, 'user/nobatches.html')
def sendrequest(request,id,jid):
    d1 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    res = Request.objects.filter(
        Q(USER=User.objects.get(LOGIN=request.session['lid']), status="approved") |
        Q(USER=User.objects.get(LOGIN=request.session['lid']), status="pending")
    )
    res1 = health.objects.filter(USER__LOGIN_id=request.session['lid'])
    res3= Batch.objects.filter(Batch_Capacity=jid)
    if res3.exists():
        return HttpResponse("<script>alert('Batch is full');window.location='/viewbatchuser#abc'</script>")
    else:
        if res1.exists():
            if res.exists():
                return HttpResponse("<script>alert('already sent');window.location='/viewbatchuser#abc'</script>")
            obj=Request()
            obj.USER=User.objects.get(LOGIN=request.session['lid'])
            obj.BATCH_id=id
            obj.time=d1
            obj.status="pending"
            obj.save()
            return HttpResponse("<script>alert('Successfully sent');window.location='/viewbatchuser#abc'</script>")
        else:
            return HttpResponse("<script>alert('Please enter health details before sending request');window.location='/uploadhealth/#abc'</script>")
def uploadhealth(request):
    res = health.objects.filter(USER_id=User.objects.get(LOGIN_id=request.session['lid'])).order_by('-id')

    if res.exists():
        return render(request, 'user/uploadhealthinfo.html',{'data': res[0]})
    else:
        return render(request, 'user/uploadhealthinfo.html')

def uploadhealth_post(request):
    height1=request.POST['textfield']
    weight1=request.POST['textfield2']
    height=float(height1)/100
    bmi1= round(float(weight1) / (height * height), 2)
    active=request.POST['select']
    foodtype1=request.POST['RadioGroup1']
    target1=request.POST['RadioGroup2']
    targetweight1=request.POST['textfield3']
    weeklytarget1=request.POST['select2']
    estimatedtime1=request.POST['textfield4']
    mcondition1=request.POST.getlist('CheckboxGroup1')
    allergies1=request.POST['textfield6']
    uid = User.objects.get(LOGIN=request.session['lid'])

    obj=health()
    obj.height=height1
    obj.weight=weight1
    obj.activelevel=active
    obj.medical=",".join(mcondition1)
    obj.bmi=bmi1
    obj.foodtype=foodtype1
    obj.target=target1
    obj.targetweight=targetweight1
    obj.estimatedtime=estimatedtime1
    obj.weeklytarget=weeklytarget1
    obj.USER=uid
    obj.allergies=allergies1

    obj.save()

    return HttpResponse("<script>window.location='/viewhealth#abc'</script>")
def viewhealth(request):
    res = health.objects.filter(USER__LOGIN_id= request.session['lid']).order_by('-id')
    if res.exists():
        return render(request, 'user/viewhealthuser.html', {'data': res[0]})
    else:
        return HttpResponse("<script>alert('Enter Health Details');window.location='/uploadhealth#abc'</script>")



def updatehealth(request,id):
    res = health.objects.get(id=id)
    return render(request,'user/updatehealth.html',{'data':res})

def updatehealth_post(request,id):
    height1 = request.POST['textfield']
    weight1 = request.POST['textfield2']
    height = float(height1) / 100
    bmi1 = round(float(weight1) / (height * height), 2)
    active = request.POST['select']
    foodtype1 = request.POST['RadioGroup1']
    target1 = request.POST['RadioGroup2']
    targetweight1 = request.POST['textfield3']
    weeklytarget1 = request.POST['select2']
    estimatedtime1 = request.POST['textfield4']
    mcondition1 = request.POST.getlist('CheckboxGroup1')
    allergies1 = request.POST['textfield6']
    health.objects.filter(id=id).update(height=height1,weight=weight1,bmi=bmi1,activelevel=active,foodtype=foodtype1,
                                        target=target1,targetweight=targetweight1,weeklytarget=weeklytarget1,estimatedtime=estimatedtime1,
                                        medical=",".join(mcondition1),allergies=allergies1)
    return HttpResponse("<script>alert('edited');window.location='/viewhealth'</script>")

def mybatch(request):
    r=Request.objects.filter(USER__LOGIN_id=request.session['lid'], status="approved")
    if r.exists():
        l=[]
        for i in r:
            res=assign.objects.filter(REQUEST=i.id)
            for ij in res:
                l.append({
                    "name":i.BATCH.Batch_title,
                    "cap": i.BATCH.Batch_Capacity,
                    "tfrom": i.BATCH.Time_from,
                    "tTo": i.BATCH.Time_to,
                    "tname": ij.TRAINER.name,
                    "id":ij.TRAINER.id,
                    "bid":i.id
                })

        return render(request,'user/mybatch.html',{'data':l})
    else:
        return HttpResponse("<script>alert('You are not assigned to any batch!!!');window.location='/userhome';</script>")


def user_exit_batch(request, id):
    Request.objects.filter(id=id).update(status="Left")
    return HttpResponse("<script>alert('Successfully left the batch');window.location='/userhome';</script>")


def viewdietplanuser(request):
    res =diet.objects.filter(USER__LOGIN_id=request.session['lid'])
    if res.exists():
        return render(request,'user/viewdietplanuser.html',{'data':res})
    else:
        return render(request,'user/nodietplan.html')

def viewtipsuser(request):
    res = tips.objects.filter(USER__LOGIN_id=request.session['lid'])
    if res.exists():
        return render(request,'user/view tips.html',{'data':res})
    else:
        return render(request,'user/notips.html')

def viewworkoutuser(request):
    res = workout.objects.filter(USER__LOGIN_id=request.session['lid'])
    if res.exists():
        return render(request,'user/view workout.html',{'data':res})
    else:
        return render(request,'user/noworkouts.html')

def calculate_bmi(request):
    if request.method == "POST":
        try:
            weight = float(request.POST.get('weight'))
            height_cm = float(request.POST.get('height'))
            height_m = height_cm / 100  # Convert height from cm to meters
            bmi = weight / (height_m ** 2)  # BMI formula

            # Determine the health category based on BMI
            if bmi < 18.5:
                category = "Underweight"
                advice = "Your BMI is below the normal range. It's important to eat a balanced diet and maintain a healthy lifestyle. Consider consulting a healthcare provider."
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight"
                advice = "Your BMI is within the normal range. Maintain a balanced diet and regular exercise to stay healthy!"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
                advice = "Your BMI is slightly above the normal range. It might be beneficial to adopt a healthier diet and increase physical activity."
            elif 30 <= bmi < 34.9:
                category = "Obesity (Class 1)"
                advice = "Your BMI indicates obesity. It is important to follow a healthier lifestyle, including a nutritious diet and regular exercise. Consult a healthcare provider for personalized advice."
            elif 35 <= bmi < 39.9:
                category = "Obesity (Class 2)"
                advice = "Your BMI falls in the severe obesity category. Consider working closely with healthcare professionals to manage your weight and reduce health risks."
            else:
                category = "Morbid Obesity (Class 3)"
                advice = "Your BMI indicates morbid obesity. This significantly increases the risk of various health issues. It is strongly advised to seek medical consultation to develop a weight management plan."

            return render(request, 'user/bmi_calculator.html', {
                'bmi': round(bmi, 2),
                'category': category,
                'advice': advice
            })
        except (ValueError, ZeroDivisionError):
            return render(request, 'user/bmi_calculator.html', {'error': 'Please enter valid numbers.'})

    return render(request, 'user/bmi_calculator.html')
