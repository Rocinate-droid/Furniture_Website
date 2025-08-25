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
    warranty = models.IntegerField(max_length=1)
    assembly = models.CharField(max_length=50,choices=assembly_choices,default="Not Required")
    customization = models.CharField(max_length=50,choices=customization_choices,default="Available")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    @property
    def total_cost(self):
        return self.product.discounted_price * self.quantity
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.quantity} * {self.product.name}' 


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