import uuid
import django_filters
from django.db import models
from django.contrib.auth.models import User
import secrets
import string
from django.utils.text import slugify

# Create your models here.

def generate_order_id(length=8, prefix="ORD"):
    chars = string.ascii_uppercase + string.digits
    return prefix + ''.join(secrets.choice(chars) for _ in range(length))

class Categorie(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="", null=False, blank=True)
    img = models.ImageField(upload_to='categories/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="", null=False, blank=True, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    assembly_choices = [
        ("Not Required", "Not Required"),
        ("Required", "Required")
    ]
    customization_choices = [
        ("Available", "Available"),
        ("Not Available", "Not Available")
    ]
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    slug = models.SlugField(default="", null=False, blank=True, unique=True)
    room_or_Product_Type = models.ForeignKey(Room, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    discounted_price = models.IntegerField()
    original_price = models.IntegerField()
    color_options = models.CharField(max_length=10)
    img = models.ImageField(upload_to='products/')
    img2 = models.ImageField(upload_to='products/')
    img3 = models.ImageField(upload_to='products/')
    warranty = models.IntegerField()
    assembly = models.CharField(max_length=50,choices=assembly_choices,default="Not Required")
    customization = models.CharField(max_length=50,choices=customization_choices,default="Available")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Review(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=15, null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    review = models.TextField(max_length=500, null=True, blank=True)
    rating = models.IntegerField()
    img = models.ImageField(upload_to='reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.customer:
            return f"{self.customer.first_name} : {self.product.name} : {self.rating}⭐"
        return f"{self.name} : {self.product.name} : {self.rating}⭐"


class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.customer:
            return self.customer.username
        return self.anonymous
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    @property
    def total_cost(self):
        if self.product:
            return self.product.discounted_price * self.quantity
        return 0
    def __str__(self):
        if self.wishlist.customer:
            return f"{self.wishlist.customer.username}'s cart item - {self.product.name if self.product else 'No product'}"
        return f"Anonymous cart item - {self.product.name if self.product else 'No product'}"

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.CharField(max_length=40, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.customer:
            return self.customer.username
        return self.anonymous
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    @property
    def total_cost(self):
        if self.product:
            return self.product.discounted_price * self.quantity
        return 0
    def __str__(self):
        if self.cart.customer:
            return f"{self.cart.customer.username}'s cart item - {self.product.name if self.product else 'No product'}"
        return f"Anonymous cart item - {self.product.name if self.product else 'No product'}"



class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Contact(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    message = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.firstname

class BillingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.CharField(max_length=40, null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    phone = models.CharField(max_length=15)
    email = models.EmailField();
    def __str__(self):
        return self.firstname
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.CharField(max_length=40, null=True, blank=True)
    billing = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, null=True, blank=True)
    is_archived = models.BooleanField(default=False, null=True, blank=True)
    ship_firstname = models.CharField(max_length=50, null=True, blank=True)
    ship_lastname = models.CharField(max_length=50, null=True, blank=True)
    ship_address = models.CharField(max_length=300, null=True, blank=True)
    ship_street = models.CharField(max_length=300, null=True, blank=True)
    ship_city = models.CharField(max_length=50, null=True, blank=True)
    ship_state = models.CharField(max_length=50, null=True, blank=True)
    ship_pincode = models.CharField(max_length=6, null=True, blank=True)
    ship_phone = models.CharField(max_length=15, null=True, blank=True)
    ship_email = models.EmailField(null=True, blank=True);
    def __str__(self):
        return self.ship_firstname
    
class Orders(models.Model):
    status = [
        ("Pending","Pending"),
        ("Failed","Failed"),
        ("Success","Success")
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_no = models.CharField(max_length=14, default=generate_order_id, unique=True, editable=False)
    razor_order_id = models.CharField(max_length=50, editable=False)
    payment_status = models.CharField(max_length=40, choices=status)
    anonymous = models.CharField(max_length=40, null=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    shipped = models.DateField(null=True, blank=True)
    delivered = models.DateField(null=True, blank=True)
    @property
    def total_order_value(self):
        total = sum(item.price for item in self.orderitem_set.all())
        if total <= 50000:
            total += 999
        return total
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    replacement_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField()
    price = models.IntegerField()
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    

class Replacement(models.Model):
    reasons = [
        ("Bought by mistake", "Bought by mistake"),
        ("Better Price available", "Better Price Available"),
        ("Performance or Quality Issue", "Performance or Quality Issue"),
        ("Item arrived too late", "Item arrived too late"),
        ("Missing parts or accessories", "Missing parts or accessories"),
        ("Wrong item was sent", "Wrong item was sent"),
        ("No longer needed", "No longer needed"),
        ("Inaccurate website description", "Inaccurate website description"),
    ]
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    individual_order = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    reason = models.CharField(max_length=40, choices=reasons)
    comments = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    picked_up = models.DateField(null=True, blank=True)
    recieved = models.DateField(null=True, blank=True)
    refund_initiated = models.DateField(null=True, blank=True)
    refund_credited = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.individual_order.product.name} x {self.individual_order.quantity}"