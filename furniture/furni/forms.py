from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import BillingAddress
from .models import ShippingAddress
from .models import Replacement
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Email'
        }
        widgets = {
            'username' : forms.EmailInput(attrs= {
                'type' : 'email'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class contactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

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
       
