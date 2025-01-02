from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from math import ceil
from django.db.models import Q
import json
from .models import Orders, Product, ContactUs

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
                                                # MENU
# ---------------------------------------------------------------------------------------

def menu(request):
    # Fetch products
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

    # Fetch offers
    offers = Offer.objects.all()

    # Render menu.html with products and offers
    return render(request, "menu.html", {
        'allProds': allProds,
        'category_filter': category_filter,
        'query': query,
        'offers': offers,
    })
# ---------------------------------------------------------------------------------------
                                             # CONTACT
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
                                                 # CHECKOUT
# ---------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------
                                                # PROFILE
# ---------------------------------------------------------------------------------------
def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    currentuser = request.user.username
    orders = Orders.objects.filter(email=currentuser)

    orders_with_details = []
    for order in orders:
        status_updates = OrderUpdate.objects.filter(order_id=order.order_id)

        # Parse the items_json into structured data
        try:
            items = json.loads(order.items_json)  # Assuming items_json is a JSON string
            structured_items = []
            for item_id, (quantity, name, price) in items.items():
                structured_items.append({
                    'name': name,
                    'quantity': quantity,
                    'price': price
                })
        except json.JSONDecodeError:
            structured_items = []

        orders_with_details.append({
            'order': order,
            'status_updates': status_updates,
            'items': structured_items
        })

    context = {"orders_with_details": orders_with_details}
    return render(request, "profile.html", context)

# ---------------------------------------------------------------------------------------
                                            # CUSTOM ADMIN
# ---------------------------------------------------------------------------------------

# @staff_member_required
# def admin_view(request):

#     users_count = User.objects.count()
#     orders_count = Orders.objects.count()
#     products_count = Product.objects.count()
#     contacts_count = ContactUs.objects.count()

#     context = {
#         'users_count': users_count,
#         'orders_count': orders_count,
#         'products_count': products_count,
#         'contacts_count': contacts_count,
#     }
#     return render(request, 'admin.html', context)


# @staff_member_required
# def admin_orders(request):
#     orders = Orders.objects.all()
#     return render(request, 'admin_orders.html', {'orders': orders})


# @staff_member_required
# def admin_products(request):
#     products = Product.objects.all()
#     return render(request, 'admin_products.html', {'products': products})


# @staff_member_required
# def admin_users(request):
#     users = User.objects.all()
#     return render(request, 'admin_users.html', {'users': users})

# ---------------------------------------------------------------------------------