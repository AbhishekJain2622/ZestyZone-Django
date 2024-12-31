import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages



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


def is_valid_password(password):
    # Validate password (at least 8 characters, include special character, and a number)
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must include at least one special character."
    if not re.search(r"\d", password):
        return "Password must include at least one number."
    return None 

def Signup(request):
    if request.method == "POST":
        get_email = request.POST.get('email')
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')

        # Validate password complexity
        password_error = is_valid_password(get_password)
        if password_error:
            messages.error(request, password_error)
            return redirect('/auth/signup/')

        if get_password != get_confirm_password:
            messages.info(request, 'Passwords do not match.')
            return redirect('/auth/signup/')

        try:
            if User.objects.filter(username=get_email).exists():
                messages.warning(request, "Email is already taken.")
                return redirect('/auth/signup/')
        except Exception as e:
            pass

        # Create user
        myuser = User.objects.create_user(get_email, get_email, get_password)
        myuser.save()

        # Authenticate and log in the user
        myuser = authenticate(username=get_email, password=get_password)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "User created and login successful.")
            return redirect('/auth/signup/')

    return render(request, 'authentication/signup.html')

def Logout(request):
    logout(request)
    messages.success(request,'logout success')
    return render(request,'authentication/login.html')




