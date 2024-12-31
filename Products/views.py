from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *
from math import ceil
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def Home(request):
    return render(request,'base.html')

def About(request):
    return render(request,'about.html')

  

def search_view(request):
    query = request.GET.get('q', '').strip()  # Ensure whitespace is removed
    results = []
    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) | Q(category__icontains=query)
        )
    return render(request, 'menu.html', {'query': query, 'results': results})

def menu(request):
    allProds = []
    category_filter = request.GET.get('category', 'all')  # Get category from query parameter
    query = request.GET.get('q', '')  # Get search query from query parameter

    if query:  # If there's a search query, filter products by name or description
        catprods = Product.objects.filter(
            Q(product_name__icontains=query) | Q(desc__icontains=query)
        )
    else:  # If there's no query, show all products (or by category)
        if category_filter != 'all':
            catprods = Product.objects.filter(category=category_filter)
        else:
            catprods = Product.objects.all()

    cats = {item.category for item in catprods}  # Get distinct categories from the filtered products
    for cat in cats:
        prod = catprods.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    return render(request, "menu.html", {'allProds': allProds, 'category_filter': category_filter, 'query': query})

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

def Ouroffer(request):
    obj=Offer.objects.all()
    context={"objs":obj}
    return render(request,'menu.html',context)

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        Order = Orders(
            items_json=items_json,
            name=name,
            amount=amount,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )
        Order.save()

        update = OrderUpdate(order_id=Order.order_id, update_desc="The order has been placed")
        update.save()

        thank = True
        return render(request, 'checkout.html', {'thank': thank})

    return render(request, 'checkout.html')

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)

    rid = ""
    for i in items:
        print(i.oid)
        myid = i.oid
        rid = myid.replace("ZestyZone", "")
        print(rid)

    status = OrderUpdate.objects.filter(order_id=int(rid))
    for j in status:
        print(j.update_desc)

    context = {"items": items, "status": status}
    return render(request, "profile.html", context)
