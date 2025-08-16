from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('home2', views.home2, name = "home-redirect"),
    path('shop', views.shop, name = "shop"),
    path('about', views.about, name = 'aboutus'),
    path('contact', views.contact, name = 'contactus'),
    path('shop/<int:cat_id>/', views.category, name = "category"),
    path('shop/<int:cat_id>/product/<int:prod_id>', views.product, name= "product")
]