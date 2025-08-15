from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('home2', views.home2, name = "home-redirect"),
    path('shop', views.shop, name = "shop"),
    path('about', views.about, name = 'aboutus'),
    path('contact', views.contact, name = 'contactus'),
    path('shop/<int:pk>/', views.category, name = "category"),
]