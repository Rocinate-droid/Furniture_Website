from django.contrib import admin

# Register your models here.

from .models import Categorie
from .models import Testimonial
from .models import Product
from .models import Contact
from .models import CartItem
from .models import DeliveryAddress
from .models import Orders
from .models import Cart
from .models import OrderItem

admin.site.register(Categorie)
admin.site.register(Testimonial)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(DeliveryAddress)
admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(OrderItem)