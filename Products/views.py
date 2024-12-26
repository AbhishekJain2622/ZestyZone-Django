from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *
from math import ceil

# Create your views here.
def Home(request):
    return render(request,'base.html')

def About(request):
    return render(request,'about.html')

from math import ceil
from django.shortcuts import render
from .models import Product

def menu(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')  # Fetch distinct categories
    cats = {item['category'] for item in catprods}       # Create a set of categories
    
    for cat in cats:
        prod = Product.objects.filter(category=cat)      # Fetch all products in this category
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))       # Calculate the number of slides (if needed)
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "menu.html", params)
# def menu(request):
#     allProds = []
#     catprods = Product.objects.values('category','id')
#     print(catprods)
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         prod= Product.objects.filter(category=cat)
#         n=len(prod)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         allProds.append([prod, range(1, nSlides), nSlides])

#     params= {'allProds':allProds}

#     return render(request,"menu.html",params)

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