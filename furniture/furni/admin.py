from django.contrib import admin

# Register your models here.

from .models import Categorie
from .models import Testimonial
from .models import Product
from .models import Contact
from .models import CartItem

admin.site.register(Categorie)
admin.site.register(Testimonial)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(CartItem)