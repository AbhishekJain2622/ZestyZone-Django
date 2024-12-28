from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *
from math import ceil
from django.db.models import Q



# Create your views here.
def Home(request):
    return render(request,'base.html')

def About(request):
    return render(request,'about.html')

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        # Adjust filter conditions based on your model fields
        results = Product.objects.filter(
            Q(product_name__icontains=query) | Q(category__icontains=query)  # Example
        )
    return render(request, 'search.html', {'query': query, 'results': results})



def menu(request):
    # Fetch all products grouped by categories
    allProds = []
    catprods = Product.objects.values('category', 'id')  # Fetch distinct categories
    cats = {item['category'] for item in catprods}       # Create a set of categories
    
    for cat in cats:
        prod = Product.objects.filter(category=cat)      # Fetch all products in this category
        n = len(prod)
        nSlides = ceil(n / 4)                            # Calculate the number of slides
        allProds.append([prod, range(1, nSlides + 1), nSlides])

    params = {'allProds': allProds}
    return render(request, "menu.html", params)

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

def Ouroffer(request):
    obj=Offer.objects.all()
    context={"objs":obj}
    return render(request,'base.html',context)

