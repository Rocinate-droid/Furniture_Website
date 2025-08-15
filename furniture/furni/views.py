import re

from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Categorie
from .models import Testimonial
from .models import Product


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
    return render(request, "furni/contact.html")

def category(request,pk):
    category = Categorie.objects.get(id=pk)
    products = Product.objects.filter(id=pk)
    for p in products:
        original_price = int(p.original_price.replace(",",""))
        discounted_price = int(p.discounted_price.replace(",",""))
        p.savings = original_price - discounted_price
        p.savings_percentage = int((p.savings / original_price ) * 100)
    context = {'category': category, 'products': products}
    return render(request, "furni/category.html", context)

def product(request,pk):
    product = Product.objects.get(id=pk)
    for p in product:
        original_price = int(p.original_price.replace(",",""))
        discounted_price = int(p.discounted_price.replace(",",""))
        p.savings = original_price - discounted_price
        p.savings_percentage = int((p.savings / original_price ) * 100)
    context = {'product': product}
    return render(request, "furni/product.html", context)