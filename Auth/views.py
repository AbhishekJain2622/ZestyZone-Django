from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def Login(request):
    return render(request,"authentication/login.html")
def Signup(request):
    return render(request,"authentication/signup.html")
def Logout(request):
    return redirect(request,"authentication/login.html")
