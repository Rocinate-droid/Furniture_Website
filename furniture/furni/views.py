from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Categorie
from .models import Testimonial
from .models import Product
from .models import Cart,CartItem
from .forms import contactForm

from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import UserChangeForm
from .forms import addressForm
import uuid


# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        if 'user_id' not in request.session:
            request.session['user_id'] = int(uuid.uuid4())
    categories = Categorie.objects.all()
    testimonials = Testimonial.objects.all()
    context = {'categories' : categories[0:3], 'testimonials' : testimonials}
    return render(request, "furni/home.html", context)

def shop(request):
    categories = Categorie.objects.all()
    context = {'categories' : categories}
    return render(request, "furni/shop.html", context )

def services(request):
    return render(request, "furni/services.html")

def about(request):
    return render(request, "furni/about.html")

def leaders(request):
    return render(request, "furni/leaders.html")

def carrers(request):
    return render(request, "furni/carrers.html")

def contact(request):
    form = contactForm(request.POST or None)
    if form.is_valid():
        contact = form.save()
        send_mail(
            'You were contacted by ' + contact.firstname + " " + contact.lastname,
            'Their phone number is ' + contact.phone + " and email is " + contact.email + "and has left you a message " + contact.message,
            'settings.EMAIL_HOST_USER',        # From
            ['sreejithcs895@gmail.com'],        # To
            fail_silently=False,
            )
        send_mail(
            "Thank you for contacting module furnitures, we'll get back to you shortly",
            "Thank you for contacting module furnitures, we'll get back to you shortly",
            'settings.EMAIL_HOST_USER',        # From
            [contact.email],        # To
            fail_silently=False,
            )
        return redirect('contactus')
    context = {'form': form }
    return render(request, "furni/contact.html", context)

def category(request, cat_id):
    category = Categorie.objects.get(id=cat_id)
    products = Product.objects.filter(category_id=cat_id)
    price = request.GET.get('price')
    sort  = request.GET.get('sort')
    if sort:
        if sort == "low_to_high":
            products = products.order_by('discounted_price')
        elif sort == "high_to_low":
            products = products.order_by('-discounted_price')
    if price:
            min_price, max_price = map(int, price.split("-"))
            products = products.filter(Q(discounted_price__gte=min_price) & Q(discounted_price__lte=max_price))
    for p in products:
        p.savings = p.original_price - p.discounted_price
        p.savings_percentage = int((p.savings / p.original_price) * 100)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("furni/product_list.html", {'products': products})
        return HttpResponse(html)
    context = {'category': category, 'products': products}
    return render(request, "furni/category.html", context)

def product(request,cat_id,prod_id):
    product = get_object_or_404(Product,id = prod_id,category_id=cat_id)
    product.savings = product.original_price - product.discounted_price
    product.savings_percentage = int((product.savings / product.original_price ) * 100)
    
    context = {'product': product}
    return render(request, "furni/product.html", context)


def view_cart(request):
    user_id = request.session.get('user_id')
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cart_items = CartItem.objects.filter(cart=cartcreated)
    else:
        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
        else:
            request.session['user_id'] = int(uuid.uuid4())
            user_id = request.session.get('user_id')
        cartcreated, created = Cart.objects.get_or_create(anonymous=user_id)
        cart_items = CartItem.objects.filter(cart=cartcreated)
    total_amount = 0
    total_original = 0
    discount = 0
    delivery = None
    grand_total = 0
    for item in cart_items:
        if item.product:
            total_original += item.product.original_price * item.quantity
            discount += (item.product.original_price - item.product.discounted_price) * item.quantity
        total_amount += item.total_cost
        grand_total += item.total_cost
    if grand_total >= 50000:
        delivery = "Free Delivery"
    else:
        delivery = 999
        grand_total += delivery
    context = {'cart_items' : cart_items, 'total_amount' : total_amount, 'total_original' : total_original, 'discount' : discount, 'delivery': delivery, 'grand_total' : grand_total }
    return render(request, "furni/cart.html", context)

def add_to_cart(request,product_id,qty):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cart_item, created2 = CartItem.objects.get_or_create(product=product,cart=cartcreated,defaults={'quantity':qty})
    else:
        cartcreated, created = Cart.objects.get_or_create(anonymous=request.session.get('user_id'))
        cart_item, created2 = CartItem.objects.get_or_create(product=product,cart=cartcreated,defaults={'quantity':qty})
    if not created2:
        cart_item.quantity += qty
        cart_item.save()
    return redirect(view_cart)


def delete_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cartProduct = CartItem.objects.get(id=cart_item_id,cart=cartcreated)
    else:
        cartcreated, created = Cart.objects.get_or_create(anonymous=request.session.get('user_id'))
        cartProduct = CartItem.objects.get(id=cart_item_id,cart=cartcreated)
    cartProduct.delete()
    return redirect(view_cart)


def update_cart(request, cart_item_id, qty):
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cartProduct = get_object_or_404(CartItem, id=cart_item_id)
        cartProduct.quantity = qty
        cartProduct.save()
        cart_items = CartItem.objects.filter(cart=cartcreated)
    else:
        cartcreated, created = Cart.objects.get_or_create(anonymous=request.session.get('user_id'))
        cartProduct = get_object_or_404(CartItem, id=cart_item_id)
        cartProduct.quantity = qty
        cartProduct.save()
        cart_items = CartItem.objects.filter(cart=cartcreated)
    total_amount = 0
    total_original = 0
    discount = 0
    delivery = None
    grand_total = 0
    for item in cart_items:
        total_original += item.product.original_price * item.quantity
        total_amount += item.total_cost
        grand_total += item.total_cost
        discount += (item.product.original_price - item.product.discounted_price) * item.quantity
    if grand_total >= 50000:
        delivery = "Free Delivery"
    else:
        delivery = 999
        grand_total += delivery
    context = {'grand_total': grand_total, 'cart_items': cart_items, 'discount': discount, 'total_original': total_original, 'delivery':delivery, 'total_amount' :total_amount}
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        item_html = render_to_string("furni/cart_list.html", {'cart_items': cart_items}),
        total_html = render_to_string("furni/cart_total.html", context )
        return JsonResponse({
            'cart_html' : item_html,
            'total_html' : total_html
        })
    return redirect(view_cart)

def loginpage(request):
    page = "login"
    context = {'page':page}
    if request.POST:
        context = {}
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is wrong")
    return render(request, 'furni/login.html',context)

def registerpage(request):
    form = CustomUserCreationForm()
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            cart, created = Cart.objects.get_or_create(customer=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    return render(request, 'furni/login.html', {'form':form})

@login_required
def logoutrequest(request):
    logout(request)
    return redirect(home)

def checkout(request):
    page = "cart_checkout"
    print("hello")
    form = addressForm(request.POST or None)
    if form.is_valid():
        address = form.save(commit=False)
        if request.user.is_authenticated:
            address.customer = request.user
        else:
            address.anonymous=request.session.get('user_id')
        address.save()
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cart_items = CartItem.objects.filter(cart=cartcreated)
    else:
        cartcreated, created = Cart.objects.get_or_create(anonymous=request.session.get('user_id'))
        cart_items = CartItem.objects.filter(cart=cartcreated)
    total_cost = 0
    grand_total = 0
    for item in cart_items:
        grand_total += item.total_cost
        total_cost += item.total_cost
    if grand_total >= 50000:
            shipping_cost = "Free Shipping"
    else:
        shipping_cost = 999
        grand_total += shipping_cost 
    context = {'total_cost': total_cost, 'cart_items': cart_items, 'shipping_cost': shipping_cost, 'page' : page, 'grand_total': grand_total, 'form' : form}
    return render(request, 'furni/checkout.html', context)

def buynow(request, product_id, qty):
    product = Product.objects.get(id=product_id)
    total_product_cost = product.discounted_price * qty
    form = addressForm(request.POST or None)
    if form.is_valid():
        address = form.save(commit=False)
        if request.user.is_authenticated:
            address.customer = request.user
        else:
            address.anonymous=request.session.get('user_id')
        address.save()
    shipping_cost = None
    total_cost = total_product_cost
    if total_product_cost >= 50000:
        shipping_cost = "Free Shipping"
    else:
        shipping_cost = 999
        total_cost = total_product_cost + shipping_cost
    context = {'product':product, 'total_cost': total_cost , 'quantity': qty, 'shipping_cost': shipping_cost, 'total_product_cost': total_product_cost}
    return render(request, 'furni/checkout.html', context)

