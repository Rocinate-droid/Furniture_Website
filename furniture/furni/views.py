
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Categories
from .models import Testimonials

# Create your views here.

categories = [
    {'id': 1, 'name': 'Sofas'},
    {'id': 2, 'name': 'Tables'},
    {'id': 3 , 'name': 'Chairs'},
    {'id': 4, 'name': 'Cots'},
    {'id': 5, 'name': 'Cupboards'},
]

def home(request):
    categories = Categories.objects.all()
    testimonials = Testimonials.objects.all()
    context = {'categories' : categories[0:3], 'testimonials' : testimonials}
    return render(request, "furni/home.html", context)

def home2(request):
    return redirect('home')

def shop(request):
    categories = Categories.objects.all()
    context = {'categories' : categories}
    return render(request, "furni/shop.html", context )

def about(request):
    return render(request, "furni/about.html")

def contact(request):
    return render(request, "furni/contact.html")

def category(request,pk):
    category = None
    for i in categories:
        if i['id'] == pk:
            category = i
        context = {'category': category}
    return render(request, "furni/product.html", context)