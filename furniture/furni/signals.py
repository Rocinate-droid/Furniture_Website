from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import DeliveryAddress, Orders, Cart


