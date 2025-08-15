from django.contrib import admin

# Register your models here.

from .models import Categorie
from .models import Testimonial
from .models import Product

admin.site.register(Categorie)
admin.site.register(Testimonial)
admin.site.register(Product)