from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Categorie
from .models import Testimonial
from .models import Product
from .models import CartItem
from .forms import contactForm
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required



# Create your views here.

categories = [
    {'id': 1, 'name': 'Sofas'},
    {'id': 2, 'name': 'Tables'},
    {'id': 3 , 'name': 'Chairs'},
    {'id': 4, 'name': 'Cots'},
    {'id': 5, 'name': 'Cupboards'},
]

def home(request):
    categories = Categorie.objects.all()
    testimonials = Testimonial.objects.all()
    context = {'categories' : categories[0:3], 'testimonials' : testimonials}
    return render(request, "furni/home.html", context)

def home2(request):
    return redirect('home')

def shop(request):
    categories = Categorie.objects.all()
    context = {'categories' : categories}
    return render(request, "furni/shop.html", context )

def about(request):
    return render(request, "furni/about.html")

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
    cart_items = CartItem.objects.all()
    total_amount = 0
    product_total_amount = 0
    for item in cart_items:
        product_total_amount = item.quantity * item.product.discounted_price
        total_amount += (item.quantity * item.product.discounted_price)
    context = {'cart_items' : cart_items, 'total_amount' : total_amount, 'product_total_amount' : product_total_amount}
    return render(request, "furni/cart.html", context)

def add_to_cart(request,product_id,qty):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, defaults={'quantity':qty })
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect(view_cart)

def delete_from_cart(request, cart_item_id):
    cartProduct = CartItem.objects.get(id=cart_item_id)
    cartProduct.delete()
    return redirect(view_cart)
