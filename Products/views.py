from .models import Orders, Product, ContactUs, OrderUpdate,Offer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from math import ceil
from .models import *
import razorpay
import json
# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
# ----------------------------------------------------------------------------
                                                   #HOME
# ----------------------------------------------------------------------------

def Home(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'base.html', {'products': products})
   
# ---------------------------------------------------------------------------
                                                 # ABOUT
# ---------------------------------------------------------------------------
def About(request):
     obj=AboutMe.objects.all()
     context={"objs":obj}
     return render(request,'about.html',context)

# -------------------------------------------------------------------------------
                                                # SEARCH 
# -----------------------------------------------------------------------------
def search_view(request):
    query = request.GET.get('q', '').strip()  # Ensure whitespace is removed
    results = []
    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) | Q(category__icontains=query)
        )
    return render(request, 'menu.html', {'query': query, 'results': results})

# ---------------------------------------------------------------------------------------
# MENU VIEW
# ---------------------------------------------------------------------------------------

def menu(request):
    allProds = []
    category_filter = request.GET.get('category', 'all')
    query = request.GET.get('q', '')

    if query:
        catprods = Product.objects.filter(
            Q(product_name__icontains=query) | Q(desc__icontains=query)
        )
    else:
        catprods = Product.objects.filter(category=category_filter) if category_filter != 'all' else Product.objects.all()

    cats = {item.category for item in catprods}
    for cat in cats:
        prod = catprods.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    offers = Offer.objects.all()

    return render(request, "menu.html", {
        'allProds': allProds,
        'category_filter': category_filter,
        'query': query,
        'offers': offers,
    })

# ---------------------------------------------------------------------------------------
# CONTACT VIEW
# ---------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------
# CHECKOUT VIEW
# ---------------------------------------------------------------------------------------

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = int(request.POST.get('amt')) * 100  # Convert to paise for Razorpay
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Create and save the order
        order = Orders(
            items_json=items_json,
            name=name,
            amount=amount // 100,  # Convert back to INR for storage
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )
        order.save()

        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{order.order_id}",
            "notes": {"internal_order_id": order.order_id},
        })

        # Update the order with Razorpay order ID
        order.oid = razorpay_order["id"]
        order.save()

        # Pass Razorpay order details to the frontend
        context = {
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount,
            "order_id": order.order_id,  # Internal order ID for tracking
            "name": name,
            "email": email,
            "phone": phone,
        }
        return render(request, 'payment.html', context)

    return render(request, 'checkout.html')

# ---------------------------------------------------------------------------------------
# PAYMENT SUCCESS VIEW
# ---------------------------------------------------------------------------------------

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')

        try:
            # Fetch the order using the Razorpay order ID
            order = Orders.objects.get(oid=razorpay_order_id)
            order.payment_id = payment_id
            order.payment_status = "Success"
            order.save()

            messages.success(request, "Payment successful! Thank you for your order.")
        except Orders.DoesNotExist:
            messages.error(request, "Order not found!")
            return redirect('/')

        # Fetch user orders
        current_user = request.user.username
        orders = Orders.objects.filter(email=current_user)

        orders_with_details = []
        for order in orders:
            status_updates = OrderUpdate.objects.filter(order_id=order.order_id)
            try:
                items = json.loads(order.items_json)
                structured_items = [{'name': v[1], 'quantity': v[0], 'price': v[2]} for k, v in items.items()]
            except json.JSONDecodeError:
                structured_items = []

            orders_with_details.append({
                'order': order,
                'status_updates': status_updates,
                'items': structured_items,
            })

        return render(request, "profile.html", {"orders_with_details": orders_with_details})

    return redirect('/')

# ---------------------------------------------------------------------------------------
# PROFILE VIEW
# ---------------------------------------------------------------------------------------

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    current_user = request.user.username
    orders = Orders.objects.filter(email=current_user)

    orders_with_details = []
    for order in orders:
        status_updates = OrderUpdate.objects.filter(order_id=order.order_id)
        try:
            items = json.loads(order.items_json)
            structured_items = [{'name': v[1], 'quantity': v[0], 'price': v[2]} for k, v in items.items()]
        except json.JSONDecodeError:
            structured_items = []

        orders_with_details.append({
            'order': order,
            'status_updates': status_updates,
            'items': structured_items,
        })

    return render(request, "profile.html", {"orders_with_details": orders_with_details})
