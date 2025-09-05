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

class orderProducts(admin.TabularInline):
    model = OrderItem
    extra = 0

class orderAdmin(admin.ModelAdmin):
    inlines = [orderProducts]
    list_display = ("__str__","created_at","total_order_value",)

class DeliveryAddressAdmin(admin.ModelAdmin):
    list_filter = ['is_archived']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally allow staff superusers to view all
        if request.user.is_superuser:
            if 'is_archived__exact' not in request.GET:
                return qs.filter(is_archived=False)
            return qs
        return qs.filter(is_archived=False)


admin.site.register(Categorie)
admin.site.register(Testimonial)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)
admin.site.register(Cart)
admin.site.register(Orders, orderAdmin)
admin.site.register(OrderItem)