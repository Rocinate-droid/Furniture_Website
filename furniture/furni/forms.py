from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import BillingAddress
from .models import ShippingAddress
from .models import Replacement
from .models import Review
from django_select2.forms import ModelSelect2Widget
from .models import Categorie,Product, Room, RoomProductType, SubProductType

class StaticSelect2Widget(ModelSelect2Widget):
    """Select2 widget that shows all results without typing."""
    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        # Always return all objects, ignoring the search term
        return self.queryset.all()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'room_or_Product_Type':StaticSelect2Widget(
                model = Room,
                attrs = {'data-minimum-results-for-search': 'Infinity'}

            ),
            'Product_Type':ModelSelect2Widget(
                model = RoomProductType,
                search_fields =['name__icontains'],
                dependent_fields={'room_or_Product_Type':'Room_Type'},
                queryset=RoomProductType.objects.all(),
            ),
            'Sub_Product':ModelSelect2Widget(
                model=SubProductType,
                search_fields=['name__icontains'],
                dependent_fields={'Product_Type':'Product_Type'},
                queryset=SubProductType.objects.all(),
            )
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']

class CustomEmailChangeForm(UserChangeForm):
    class Meta:
        model = User
        password = None
        fields = ['email']

class CustomNameChangeForm(UserChangeForm):
    class Meta:
        model = User
        password = None
        fields = ['first_name',"last_name"]

class contactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class addressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ['customer', 'anonymous', 'is_archived']
        fields = '__all__'

class shippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ['customer', 'anonymous', 'is_archived', 'billing']
        fields = '__all__'

class replacementForm(forms.ModelForm):
    class Meta:
        model = Replacement
        fields = ['reason', 'comments']

class reviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review','rating','title','img','name']
