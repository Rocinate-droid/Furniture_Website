from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='categories/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Testimonials(models.Model):
    name = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    def __str__(self):
        return self.name