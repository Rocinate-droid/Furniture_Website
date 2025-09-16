from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import BillingAddress
from .models import ShippingAddress
from .models import Replacement
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
       
