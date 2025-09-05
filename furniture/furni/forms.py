from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import DeliveryAddress
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
        model = DeliveryAddress
        exclude = ['customer', 'anonymous', 'is_archived']
        fields = '__all__'
