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
    return HttpResponse("<script>alert('added');window.location='/viewbatch#abc'</script>")
def updatetraineradmin(request,id):
    res=Trainer.objects.get(id=id)
    return render(request,'admin/edit Trainer.html',{'data':res,'id':id})
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
def viewfeedback(request):
    res=feedback.objects.all()
    if res.exists():
        return render(request, 'admin/view feedback.html',{'data':res})
    else:
        return render(request,'admin/nofeedback.html')
def viewrequest(requset,id):
    res = Request.objects.filter(BATCH=Batch.objects.get(id=id),status="pending")
    if res.exists():
        return render(requset, 'admin/View Request.html',{'data':res})
    else:
        return render(requset,'admin/norequest.html')

#trainer
def viewprofile(request):
    res=Trainer.objects.get(LOGIN=request.session['lid'])
    return render(request,'trainer/view profile.html',{'data':res})
def trainerhome(request):
    return render(request,'trainerIndex.html')


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
