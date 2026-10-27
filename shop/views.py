from django.shortcuts import render, get_object_or_404
from .models import Product, Contact, Orders, OrderUpdate, Address
from math import ceil
import json
from django.contrib.auth.decorators import login_required  # <-- Add this import
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import CartItem
from .forms import AddressForm
from django.contrib import messages
from datetime import timedelta

# Create your views here.
from django.http import HttpResponse


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank=False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html', {'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

@login_required
def add_to_cart(request):

    if request.method == "POST":

        product_id = request.POST.get("product_id")

        try:
            product = Product.objects.get(id=product_id)

            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product
            )

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({
                "status": "success"
            })

        except Product.DoesNotExist:

            return JsonResponse({
                "status": "error"
            })

    return JsonResponse({
        "status": "invalid"
    })


@login_required
def cart_count(request):

    items = CartItem.objects.filter(
        user=request.user
    )

    count = sum(item.quantity for item in items)

    return JsonResponse({
        "count": count
    })




@login_required(login_url='signup')
def checkout(request):

    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('/shop/cart/')

    addresses = Address.objects.filter(user=request.user)
    if not addresses.exists():
        return redirect("/shop/add-address/")
    default_address = addresses.filter(is_default=True).first()

    total_price = 0

    for item in cart_items:
        item.line_total = item.product.price * item.quantity
        total_price += item.line_total

    if request.method == "POST":

        address_id = request.POST.get("address")

        try:
            selected_address = Address.objects.get(
                id=address_id,
                user=request.user
            )
        except Address.DoesNotExist:
            messages.error(request, "Please select a valid delivery address.")
            return redirect("/shop/checkout/")

        items_json = {}

        for item in cart_items:
            items_json[item.product.product_name] = {
                "quantity": item.quantity,
                "price": item.product.price
            }

        order = Orders(
            user=request.user,
            items_json=json.dumps(items_json),

            name=selected_address.full_name,
            email=request.user.email,

            address=selected_address.address_line1 +
                    " " +
                    selected_address.address_line2,

            city=selected_address.city,
            state=selected_address.state,
            zip_code=selected_address.zip_code,
            phone=selected_address.phone,
        )

        order.save()

       
        cart_items.delete()

        return redirect(
    "OrderSuccess",
    order_id=order.order_id
)

    return render(
    request,
    "shop/checkout.html",
    {
        "cart_items": cart_items,
        "total_price": total_price,
        "addresses": addresses,
        "default_address": default_address
    }
)

@login_required(login_url='login')
def order_success(request, order_id):

    order = Orders.objects.get(
        order_id=order_id,
        user=request.user
    )

    return render(
        request,
        "shop/order_success.html",
        {
            "order": order
        }
    )

@login_required(login_url='login')
def add_address(request):

    if request.method == "POST":

        # If this is the user's first address, make it default
        is_default = not Address.objects.filter(user=request.user).exists()

        address = Address(
            user=request.user,
            address_title=request.POST.get("address_title"),
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            address_line1=request.POST.get("address_line1"),
            address_line2=request.POST.get("address_line2"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            zip_code=request.POST.get("zip_code"),
            is_default=is_default
        )

        address.save()

        return redirect("/shop/checkout/")

    return render(request, "shop/add_address.html")

@login_required(login_url='login')
def addresses(request):

    addresses = Address.objects.filter(
        user=request.user
    )

    return render(
        request,
        "shop/addresses.html",
        {
            "addresses": addresses
        }
    )

@login_required(login_url='login')
def delete_address(request, id):

    address = get_object_or_404(
        Address,
        id=id,
        user=request.user
    )

    was_default = address.is_default

    address.delete()

    if was_default:

        new_default = Address.objects.filter(
            user=request.user
        ).first()

        if new_default:

            new_default.is_default = True
            new_default.save()

    return redirect("/shop/addresses/")

@login_required(login_url='login')
def set_default_address(request, id):

    Address.objects.filter(
        user=request.user
    ).update(is_default=False)

    address = get_object_or_404(
        Address,
        id=id,
        user=request.user
    )

    address.is_default = True

    address.save()

    return redirect("/shop/addresses/")

@login_required(login_url='login')
def edit_address(request, id):

    address = get_object_or_404(
    Address,
    id=id,
    user=request.user
)

    if request.method == "POST":

        address.address_title = request.POST.get("address_title")

        address.full_name = request.POST.get("full_name")

        address.phone = request.POST.get("phone")

        address.address_line1 = request.POST.get("address_line1")

        address.address_line2 = request.POST.get("address_line2")

        address.city = request.POST.get("city")

        address.state = request.POST.get("state")

        address.zip_code = request.POST.get("zip_code")

        address.save()

        return redirect("/shop/addresses/")

    return render(
        request,
        "shop/edit_address.html",
        {
            "address": address
        }
    )

# 1. Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log them in after signing up
            return redirect('/')  # Send them straight to checkout
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

# 2. Login View (Fixed to use ShopHome)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # If they were kicked here from checkout, send them back to checkout
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('ShopHome')  # <-- Changed from 'index' to 'ShopHome'
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

# 3. Logout View (Fixed to use ShopHome)
def logout_view(request):
    logout(request)
    return redirect('ShopHome')  # <-- Changed from 'index' to 'ShopHome'

@login_required
def cart(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    total_price = 0

    for item in cart_items:
        total_price += item.product.price * item.quantity

    context = {
        "cart_items": cart_items,
        "total_price": total_price
    }

    return render(
        request,
        "shop/cart.html",
        context
    )

@login_required
def increase_cart(request, item_id):

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('/shop/cart/')


@login_required
def decrease_cart(request, item_id):

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    else:

        cart_item.delete()

    return redirect('/shop/cart/')


@login_required
def remove_cart(request, item_id):

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('/shop/cart/')

@login_required(login_url='login')
def my_orders(request):

    orders = Orders.objects.filter(
        user=request.user
    ).order_by("-order_date")

    return render(
        request,
        "shop/my_orders.html",
        {
            "orders": orders
        }
    )

@login_required(login_url='login')
def my_orders(request):

    orders = Orders.objects.filter(
        user=request.user
    ).order_by("-order_date")

    return render(
        request,
        "shop/my_orders.html",
        {
            "orders": orders
        }
    )

@login_required(login_url='login')
def order_details(request, order_id):

    order = get_object_or_404(
        Orders,
        order_id=order_id,
        user=request.user
    )

    items = json.loads(order.items_json)
    grand_total = 0

    for product_name, details in items.items():

     details["line_total"] = (
        details["quantity"] * details["price"]
    )

    grand_total += details["line_total"]

    updates = OrderUpdate.objects.filter(
    order_id=order.order_id
    ).order_by("-update_id")

    status_list = list(
    updates.values_list("update_desc", flat=True)
    )

    if updates.exists():
       latest_update = updates.first()
       current_status = latest_update.update_desc
    else:
      current_status = "Processing"
    expected_delivery = order.order_date + timedelta(days=5)
    return render(
        request,
        "shop/order_details.html",
        {
            "order": order,
            "items": items,
            "updates": updates,
            "current_status": current_status,
            "status_list": status_list,
            "expected_delivery": expected_delivery,
            "grand_total": grand_total,
        }
    )