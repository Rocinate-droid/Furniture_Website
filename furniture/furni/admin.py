from django.contrib import admin

# Register your models here.

from .models import Categorie, Room
from .models import Testimonial, Review
from .models import Product, RoomProductType, SubProductType
from .models import Contact
from .models import CartItem
from .models import BillingAddress, ShippingAddress
from .models import Orders
from .models import Cart
from .models import Wishlist
from.forms import ProductForm
from .models import OrderItem, Replacement




class orderProducts(admin.TabularInline):
    model = OrderItem
    extra = 0

class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}

class CategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    prepopulated_fields = {"slug" : ("name",)}

class orderAdmin(admin.ModelAdmin):
    inlines = [orderProducts]
    list_display = ("__str__","created_at","total_order_value","order_no")
    readonly_fields = ['order_no', 'total_order_value', 'created_at',"razor_order_id"]

class replacementAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']

class BillingAddressAdmin(admin.ModelAdmin):
    list_filter = ['is_archived']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally allow staff superusers to view all
        if request.user.is_superuser:
            if 'is_archived__exact' not in request.GET:
                return qs.filter(is_archived=False)
            return qs
        return qs.filter(is_archived=False)


admin.site.register(Categorie,CategorieAdmin)
admin.site.register(Testimonial)
admin.site.register(Product, ProductAdmin)
admin.site.register(RoomProductType)
admin.site.register(SubProductType)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Cart)
admin.site.register(Orders, orderAdmin)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Room, RoomAdmin)
admin.site.register(Replacement, replacementAdmin)