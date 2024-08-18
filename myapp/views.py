from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Login, User, Request

def loginn(request):
    return render(request, 'admin/login.html')

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

def register(request):
    return render(request, "user/register.html")

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
