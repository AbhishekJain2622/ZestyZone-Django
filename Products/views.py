from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *

# Create your views here.
def Home(request):
    return render(request,'base.html')

def About(request):
    return render(request,'about.html')

def menu(request):
    return render(request,'menu.html')


def Contact(request):
    if request.method == "POST":
        fname = request.POST.get('name')
        femail = request.POST.get('email')
        fphoneno = request.POST.get('num')
        fdesc = request.POST.get('desc')

        query = ContactUs(name=fname, email=femail, phonenumber=fphoneno, description=fdesc)
        query.save()
        messages.success(request, "Thanks for contacting us. We will get back to you soon!")

        return redirect('/contact/')

    return render(request, 'contact.html')