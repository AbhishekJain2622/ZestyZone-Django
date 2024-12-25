from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def Login(request):
    if request.method=="POST":
        get_email=request.POST.get('email')
        get_password=request.POST.get('pass1')
        myuser= authenticate(username=get_email,password=get_password)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/auth/login')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'authentication/login.html')
    
def Signup(request):
    if request.method=="POST":
        get_email=request.POST.get('email')
        get_password=request.POST.get('pass1')
        get_confirm_password=request.POST.get('pass2')
        if get_password!=get_confirm_password:
            messages.info(request,'Password is not matching')
            return redirect('/auth/signup/')
        
        try:
            if User.objects.get(username=get_email):
                messages.warning(request,"Email is Taken")
                return redirect('/auth/signup/')
        except Exception as identifier:
            pass
        myuser=User.objects.create_user(get_email,get_email,get_password)
        myuser.save()

        myuser= authenticate(username=get_email,password=get_password)

        if myuser is not None:

            login(request,myuser)
            messages.success(request,"User Created & Login Success")
            return redirect('/auth/signup/')

        
    return render(request,'authentication/signup.html')
def Logout(request):
    logout(request)
    messages.success(request,'logout success')
    return render(request,'authentication/login.html')
   