from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import razorpay
import traceback
from django.conf import settings
from .models import Categorie, Room
from .models import Testimonial, Review
from .models import Product
from .models import Cart,CartItem, Wishlist, WishlistItem
from .forms import contactForm
from .models import Orders
from django.views.decorators.csrf import csrf_exempt
from .models import OrderItem
from .models import BillingAddress
from .models import Replacement
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .forms import addressForm, shippingAddressForm, replacementForm, CustomEmailChangeForm, CustomNameChangeForm, reviewForm
import uuid
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


# Create your views here.


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def home(request):
    if not request.user.is_authenticated:
        if 'user_id' not in request.session:
            request.session['user_id'] = int(uuid.uuid4())
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
    categories = Categorie.objects.all()
    testimonials = Testimonial.objects.all()
    products = Product.objects.all()
    for product in products:
        product.savings = product.original_price - product.discounted_price
        product.savings_percentage = int((product.savings / product.original_price ) * 100)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("furni/new_launches.html", {'products': products})
        return HttpResponse(html) 
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wish_items = WishlistItem.objects.filter(wishlist=wishlistcreated).values_list('product_id', flat=True)
        context = {'categories' : categories, 'testimonials' : testimonials, 'products': products, 'wish_items':list(wish_items), 'cart_items': cart_items}
    else:
        context = {'categories' : categories, 'testimonials' : testimonials, 'products': products, 'cart_items': cart_items}
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

def purchase_returns(request):
    return render(request, "furni/purchase-returns.html")

def terms_conditions(request):
    return render(request, "furni/terms-conditions.html")

def shipping_delivery(request):
    return render(request, "furni/shipping-delivery.html")

def privacy_policy(request):
    return render(request, "furni/privacy-policy.html")

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

def category(request, cat_name):
    category = Categorie.objects.get(slug=cat_name)
    products = Product.objects.filter(category__name=category.name)
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

def rooms(request,room_type):
    room = Room.objects.get(slug=room_type)
    products = Product.objects.filter(room_or_Product_Type=room.id)
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
    context = {'products': products, 'current_room' : room_type}
    return render(request, "furni/category.html", context)

def product_search(request):
    search_word = request.GET.get("search_word")
    products = Product.objects.all()
    if search_word != None:
        print("gekko")
        search_word.strip()
        products = products.filter(Q(name__icontains=search_word) | Q(category__name__icontains=search_word) | Q(room_or_Product_Type__name__icontains=search_word))
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
    context = {'products' : products, "search_word" : search_word,}
    return render(request, "furni/category.html", context)


def product(request,cat_id,prod_id):
    category = Categorie.objects.get(slug=cat_id)
    selected_product = get_object_or_404(Product,slug=prod_id)
    product = get_object_or_404(Product,id = selected_product.id,category_id=category.id)
    product.savings = product.original_price - product.discounted_price
    product.savings_percentage = int((product.savings / product.original_price ) * 100)
    reviews = Review.objects.filter(product=product)
    sort  = request.GET.get('sort_order')
    
    review_dict = {"five_star":0,"four_star":0,"three_star":0,"two_star":0,"one_star":0}
    overall_rating = 0.0
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                old_review = Review.objects.get(customer=request.user, product=selected_product.id)
                form = reviewForm(request.POST, request.FILES, instance=old_review)
            except Review.DoesNotExist:
                form = reviewForm(request.POST, request.FILES)
        else:
            form = reviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.customer = request.user
            else:
                review.name = request.POST.get("name")
        review.product = product
        review.save()
    else:
        if request.user.is_authenticated:
            try:
                old_review = Review.objects.get(customer=request.user, product=selected_product.id)
                form = reviewForm(instance=old_review)
            except Review.DoesNotExist:
                form = reviewForm()
        else:
            form = reviewForm()
    for review in reviews:
        if review.rating == 5:
            review_dict["five_star"] = review_dict["five_star"] + 1
        elif review.rating == 4:
            review_dict["four_star"] = review_dict["four_star"] + 1
        elif review.rating == 3:
            review_dict["three_star"] = review_dict["three_star"] + 1
        elif review.rating == 2:
            review_dict["two_star"] = review_dict["two_star"] + 1
        elif review.rating == 1:
            review_dict["one_star"] = review_dict["one_star"] + 1
    if reviews.count() > 0:
        overall_rating = ((5 * review_dict["five_star"]) + (4 * review_dict["four_star"]) + (3 * review_dict["three_star"]) + (2 * review_dict["two_star"]) + (1 * review_dict["one_star"]))/reviews.count()
    reviews = reviews.order_by('-created_at')
    if sort:
        if sort == "highest_rating":
            reviews = reviews.order_by('-rating')
        elif sort == "lowest_rating":
            reviews = reviews.order_by('rating')
        else:
            reviews = reviews.order_by('-created_at')
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("furni/review-cards.html", {'reviews': reviews})
        return HttpResponse(html)
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wish_items = WishlistItem.objects.filter(wishlist=wishlistcreated).values_list('product_id', flat=True)
        
        context = {'product': product,'form':form , 'reviews':reviews, 'overall_rating':round(overall_rating), "review_dict":review_dict, "wish_items":wish_items}
    else:
        context = {'product': product,'form':form , 'reviews':reviews, 'overall_rating':round(overall_rating), "review_dict":review_dict}
    return render(request, "furni/product.html", context)


def view_wishlist(request):
    user_id = request.session.get('user_id')
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wish_items = WishlistItem.objects.filter(wishlist=wishlistcreated)
    else:
        return redirect('loginpage')
    context = {'wish_items' : wish_items,}
    return render(request, "furni/wishlist.html", context)

def add_to_wishlist(request,product_id,qty):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wish_item, created2 = WishlistItem.objects.get_or_create(product=product,wishlist=wishlistcreated,defaults={'quantity':qty})
    if not created2:
        wish_item.quantity += qty
        wish_item.save()
    return redirect(view_wishlist)

def delete_from_wishlist(request, wish_item_id):
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wishitem = WishlistItem.objects.get(product__id=wish_item_id,wishlist=wishlistcreated)
    wishitem.delete()
    return redirect(view_wishlist)

def update_wishlist(request, wish_item_id, qty):
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wishitem = get_object_or_404(WishlistItem, id=wish_item_id)
        wishitem.quantity = qty
        wishitem.save()
        wish_items = WishlistItem.objects.filter(wishlist=wishlistcreated)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("furni/wishlist_items.html", {'wish_items': wish_items})
            return HttpResponse(html)
    return redirect(view_wishlist)

def transfer_to_cart(request, wish_item_id):
    if request.user.is_authenticated:
        wishlistcreated, created = Wishlist.objects.get_or_create(customer=request.user)
        wishitem = get_object_or_404(WishlistItem, wishlist=wishlistcreated, id=wish_item_id)
        cartcreated, created2 = Cart.objects.get_or_create(customer=request.user)
        cart_item, cartitemcreated = CartItem.objects.get_or_create(cart=cartcreated,product=wishitem.product,defaults={'quantity': wishitem.quantity})
        if not cartitemcreated:
            cart_item.quantity += wishitem.quantity 
            cart_item.save()
        wishitem.delete()
        wish_items = WishlistItem.objects.filter(wishlist=wishlistcreated)
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
    context = {'cart_items' : cart_items, 'total_amount' : total_amount, 'total_original' : total_original, 'discount' : discount, 'delivery': delivery, 'grand_total' : grand_total }
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        wishlist_html = render_to_string("furni/wishlist_items.html", {'wish_items': wish_items}),
        cart_html = render_to_string("furni/quick-cart.html", context )
        return JsonResponse({
            'wishlist_html' : wishlist_html,
            'cart_html' : cart_html
        })
        html = render_to_string("furni/wishlist_items.html", {'wish_items': wish_items})
        return HttpResponse(html)
    return redirect(view_cart)

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
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("furni/quick-cart.html", {'cart_items': cart_items, 'grand_total': grand_total, 'cart_items': cart_items, 'discount': discount, 'total_original': total_original, 'delivery':delivery, 'total_amount' :total_amount,})
        return HttpResponse(html)
    return redirect(view_cart)


def delete_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cartProduct = CartItem.objects.get(id=cart_item_id,cart=cartcreated)
    else:
        cartcreated, created = Cart.objects.get_or_create(anonymous=request.session.get('user_id'))
        cartProduct = CartItem.objects.get(id=cart_item_id,cart=cartcreated)
    cartProduct.delete()
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
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("furni/quick-cart.html", {'cart_items': cart_items, 'grand_total': grand_total, 'cart_items': cart_items, 'discount': discount, 'total_original': total_original, 'delivery':delivery, 'total_amount' :total_amount,})
        return HttpResponse(html)

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
    context = {'grand_total': grand_total, 'cart_items': cart_items, 'discount': discount, 'total_original': total_original, 'delivery':delivery, 'total_amount' :total_amount}
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("furni/quick-cart.html", {'cart_items': cart_items, 'grand_total': grand_total, 'cart_items': cart_items, 'discount': discount, 'total_original': total_original, 'delivery':delivery, 'total_amount' :total_amount,})
        return HttpResponse(html)
        template_name = request.headers.get('X-Template-Type', 'default')
        if template_name == "quick-cart":
            item_html = render_to_string("furni/quick_cart_list.html", {'cart_items': cart_items}),
            total_html = render_to_string("furni/quick_cart_total.html", context )
            return JsonResponse({
                'cart_html' : item_html,
                'total_html' : total_html
            })
        else:
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
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Password is Wrong")
            return redirect('loginpage')
    return render(request, 'furni/login.html',context)

def registerpage(request):
    form = CustomUserCreationForm()
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.username
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

def create_order(request):
    if request.method == 'POST':
        form = addressForm(request.POST or None)
        shipping = shippingAddressForm(request.POST or None)
        ship = None
        page = request.GET.get('page')
        name = None
        phone = None
        email = None
        if form.is_valid():
            address = form.save(commit=False)
            if request.user.is_authenticated:
                address.customer = request.user
            else:
                address.anonymous=request.session.get('user_id')
            address.save()
            name = f"{address.firstname} {address.lastname}"
            phone = address.phone
            email = address.email
            if shipping.has_changed():
                if shipping.is_valid():
                    shippingAddress = shipping.save(commit=False)
                    if request.user.is_authenticated:
                        shippingAddress.customer = request.user
                    else:
                        shippingAddress.anonymous = request.session.get('user_id')
                    shippingAddress.billing = address
                    shippingAddress.save()
                    ship = shippingAddress 
            if page == "cart_checkout":
                if request.user.is_authenticated:
                    cartcreated, created = Cart.objects.get_or_create(customer=request.user)
                    cart_items = CartItem.objects.filter(cart=cartcreated)
                    order = Orders.objects.create(customer=request.user, billing_address=address, shipping_address=ship)
                    orderno = order.order_no
                else:
                    cartcreated, created = Cart.objects.get_or_create(anonymous=request.session.get('user_id'))
                    cart_items = CartItem.objects.filter(cart=cartcreated)
                    order = Orders.objects.create(anonymous=request.session.get('user_id'), billing_address=address, shipping_address=ship)
                    orderno = order.order_no
                for cart_item in cart_items:
                    OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, price=cart_item.total_cost)
            elif page == "buy_checkout":
                product_id = request.GET.get('product')
                passed_product = Product.objects.get(id=product_id)
                qty = request.GET.get('quantity')
                total_product_cost = request.GET.get('total_product_cost')
                if request.user.is_authenticated:
                    order = Orders.objects.create(customer=request.user, billing_address=address , shipping_address=ship)
                    OrderItem.objects.create(order=order, product=passed_product, quantity=qty, price=total_product_cost)
                    orderno = order.order_no
                else:
                    order = Orders.objects.create(anonymous=request.session.get('user_id'), billing_address=address , shipping_address=ship)
                    OrderItem.objects.create(order=order, product=passed_product, quantity=qty, price=total_product_cost)
                    orderno = order.order_no
            razorpay_order = razorpay_client.order.create(dict(amount=order.total_order_value * 100,
                                                        currency="INR",
                                                        payment_capture='0'))
            razorpay_order_id = razorpay_order['id']
            order.razor_order_id = razorpay_order_id
            order.payment_status = "Pending"
            order.save()
            callback_url = "/paymenthandler/"
            if page == "cart_checkout":
                context = {'razorpay_order_id':razorpay_order_id, 'razorpay_merchant_key':settings.RAZOR_KEY_ID, 'razorpay_amount':(order.total_order_value * 100), 'currency':"INR", 'callback_url':callback_url,'orderno' : orderno, 'cartcreated':cartcreated}
            else:
                context = {'razorpay_order_id':razorpay_order_id, 'razorpay_merchant_key':settings.RAZOR_KEY_ID, 'razorpay_amount':(order.total_order_value * 100), 'currency':"INR", 'callback_url':callback_url,'orderno' : orderno}

            return JsonResponse( {
                "razorpay_order_id":razorpay_order_id,
                "razorpay_merchant_key":settings.RAZOR_KEY_ID,
                "razorpay_amount":(order.total_order_value * 100),
                "currency":"INR", 
                'callback_url':callback_url,
                'orderno' : orderno,
                'name' : name,
                'phone' : phone,
                'email' : email,
            })

def checkout(request):
    page = "cart_checkout"
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
    if grand_total >= 49999:
            shipping_cost = "Free Shipping"
    else:
        shipping_cost = 999
        grand_total += shipping_cost 
    context = {'total_cost': total_cost, 'cart_items': cart_items, 'shipping_cost': shipping_cost, 'page' : page, 'grand_total': grand_total}
    return render(request, 'furni/checkout.html', context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            if 'cartcreated' in request.POST:
                cartcreated = request.POST.get('cartcreated','')
            order = Orders.objects.get(razor_order_id=razorpay_order_id)
            print(order)
            order_no = order.order_no
            raz_amount = order.total_order_value
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount =  int(raz_amount * 100) # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    order.payment_status = "Success"
                    if cartcreated:
                        CartItem.objects.filter(cart=cartcreated).delete()
                    order.save()
                    # render success page on successful caputre of payment
                    return render(request, 'furni/thankyou.html', {"orderno": order_no})
                except:
                    order.payment_status = "Failed"
                    if cartcreated:
                        CartItem.objects.filter(cart=cartcreated).delete()
                    order.save()
                    # if there is an error while capturing payment.
                    return render(request, 'furni/failure.html')
            else:
                order.payment_status = "Failed"
                if cartcreated:
                        CartItem.objects.filter(cart=cartcreated).delete()
                order.save()
                # if signature verification fails.
                return render(request, 'furni/failure.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


def buynow(request, product_id, qty):
    page = "buy_checkout"
    product = Product.objects.get(id=product_id)
    total_product_cost = product.discounted_price * qty
    form = addressForm(request.POST or None)
    shipping = shippingAddressForm(request.POST or None)
    shipping_cost = None
    total_cost = total_product_cost
    if total_product_cost >= 49999:
        shipping_cost = "Free Shipping"
    else:
        shipping_cost = 999
        total_cost = total_product_cost + shipping_cost
    context = {'product':product, 'total_cost': total_cost , 'quantity': qty, 'shipping_cost': shipping_cost, 'total_product_cost': total_product_cost,'form': form,
        'shipping': shipping, 'page': page}
    return render(request, 'furni/checkout.html', context)

@login_required
def profile(request):
    context = {"user": request.user}
    return render(request, 'furni/profile.html', context)

@login_required
def edit_account(request):
    context = {"user": request.user}
    return render(request, 'furni/user_edit.html', context)

@login_required
def edit_password(request):
    context = {"page": "edit_password"}
    if request.method == "POST":
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("passwordsuccesspage")
        else:
            return render(request, "furni/edit_cred.html", {"form":form, "page": "edit_password"})
    return render(request, "furni/edit_cred.html", context)

@login_required
def edit_email(request):
    form = CustomEmailChangeForm(instance=request.user)
    if request.method == "POST":
        form = CustomEmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            return redirect("emailsuccesspage")   
        else:
            return render(request, "furni/edit_cred.html", {"form":form, "page": "edit_email"})
             
    context = {"page": "edit_email", "form":form}   
    return render(request, "furni/edit_cred.html", context)


@login_required
def edit_name(request):
    form = CustomNameChangeForm(instance=request.user)
    if request.method == "POST":
        form = CustomNameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("namesuccesspage")
        else:
            return render(request, "furni/edit_cred.html", {"form":form, "page": "edit_name"}) 
    context = {"page": "edit_name", "form":form}   
    return render(request, "furni/edit_cred.html", context)

@login_required
def passwordsuccesspage(request):
    return render(request, "furni/success.html", {"page":"password_success"})

@login_required
def emailsuccesspage(request):
    return render(request, "furni/success.html", {"page":"email_success"})

@login_required
def namesuccesspage(request):
    return render(request, "furni/success.html", {"page":"name_success"})

@login_required
def orders(request):
    context = {}
    returndatelist = {}
    if request.user.is_authenticated:
        orders = Orders.objects.filter(customer=request.user)
        if orders.exists():
            orders = orders.order_by("-created_at")
            for order in orders:
                if order.delivered:
                    returndate = order.delivered
                    key = order.id
                    newdate = returndate + timedelta(days=5)
                    returndatelist[key] = newdate
            context = {"orders": orders, "returndatelist": returndatelist}
        else:
            orders = "No orders"
    return render(request, "furni/orders.html", context)

@login_required
def indiv_orders(request, order_id):
    context = {}
    returndate = []
    subtotal = 0
    shipping = None
    total = 0
    discount = 0
    actualtotal = 0
    returndate = None
    currentdate = date.today()
    if request.user.is_authenticated:
        orders = Orders.objects.get(customer=request.user, id=order_id)
        replacement = Replacement.objects.filter(order=orders)
        for item in orders.products.all():
            matching_item = orders.orderitem_set.get(product=item.id)
            subtotal += item.original_price * matching_item.quantity
            actualtotal += item.discounted_price
            discount += (item.original_price - item.discounted_price) * matching_item.quantity
        if actualtotal <= 50000:
            shipping = 999
        else:
            shipping = 0
        total = subtotal + shipping
        if orders.delivered:
            returndate = orders.delivered
            returndate = returndate + timedelta(days=5)
        context = {"orders": orders, "subtotal": subtotal, "shipping":shipping, "total":total, "discount": discount, "returndate": returndate, "currentdate":currentdate, "replacement":replacement}
    return render(request, "furni/view_order.html", context)

def single_order(request, order_no, email_id):
    context = {}
    returndate = []
    subtotal = 0
    shipping = None
    total = 0
    discount = 0
    actualtotal = 0
    orders = Orders.objects.get(billing_address__email=email_id, order_no=order_no)
    replacement = Replacement.objects.filter(order=orders)
    returndate = None
    currentdate = date.today()
    for item in orders.products.all():
        matching_item = orders.orderitem_set.get(product=item.id)
        subtotal += item.original_price * matching_item.quantity
        actualtotal += item.discounted_price
        discount += (item.original_price - item.discounted_price) * matching_item.quantity
    if actualtotal <= 50000:
        shipping = 999
    else:
        shipping = 0
    total = subtotal + shipping
    if orders.delivered:
        returndate = orders.delivered
        returndate = returndate + timedelta(days=5)
    context = {"orders": orders, "subtotal": subtotal, "shipping":shipping, "total":total, "discount": discount, "returndate": returndate, "currentdate":currentdate,  "replacement":replacement}
    return render(request, "furni/view_order.html", context)

def returns(request, order_id, order_item_id):
    order = Orders.objects.get(id=order_id)
    email = order.billing_address.email
    matching_item = order.orderitem_set.get(product=order_item_id)
    form = replacementForm(request.POST or None)
    if form.is_valid():
        replacement = form.save(commit=False)
        replacement.order = order
        replacement.individual_order = matching_item
        replacement.save()
        matching_item.replacement_ordered = True
        matching_item.save()
        return redirect('home')
    returndate = None
    currentdate = date.today()
    if order.delivered:
        returndate = order.delivered
        returndate = returndate + timedelta(days=5)
    context = {"matching_item":matching_item, "returndate":returndate, "currentdate":currentdate}
    return render(request, "furni/return.html", context)

@login_required(login_url="login")
def address(request):
    addresses = BillingAddress.objects.filter(customer=request.user, is_archived=False)
    context = {'addresses': addresses}
    return render(request, "furni/address.html", context)

@login_required(login_url="login")
def delete_address(request, address_id):
    address = BillingAddress.objects.get(customer=request.user,id=address_id)
    address.is_archived = True
    address.save()
    return redirect('address')

@login_required(login_url="login")
def add_address(request):
    form = addressForm(request.POST or None)
    if form.is_valid():
        address = form.save(commit=False)
        address.customer = request.user
        form.save()
        return redirect('address')
    return render(request,'furni/add_address.html')

@login_required(login_url="login")
def edit_address(request, address_id):
    editaddress = BillingAddress.objects.get(customer=request.user, id=address_id)
    form = addressForm(instance=editaddress)
    context = {"form": form}
    if request.method == 'POST':
        form = addressForm(request.POST,instance=editaddress)
        if form.is_valid():
            form.save()
        return redirect('address')
    return render(request,'furni/edit_address.html', context)

@receiver(user_logged_in)
def transfer_cart_to_user(request, user, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    user_id = request.session.get('user_id')
    temp_cart = get_object_or_404(Cart,anonymous=user_id)
    if temp_cart:
        custCart, created = Cart.objects.get_or_create(customer=user)
        old_cart_items = CartItem.objects.filter(cart=temp_cart)
        for item in old_cart_items:
            new_cart_items, created2 = CartItem.objects.get_or_create(cart=custCart, product=item.product,defaults={'quantity':item.quantity} )
            if not created2:
                new_cart_items.quantity += item.quantity
                new_cart_items.save()
        custCart.save()
        temp_cart.delete()
        del user_id

