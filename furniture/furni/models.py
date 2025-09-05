import uuid
import django_filters
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categorie(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='categories/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
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
    def __str__(self):
        return self.name
    

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

class DeliveryAddress(models.Model):
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
    
class Orders(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    anonymous = models.CharField(max_length=40, null=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
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
    quantity = models.IntegerField()
    price = models.IntegerField()
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
