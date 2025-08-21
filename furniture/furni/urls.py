from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('home2', views.home2, name = "home-redirect"),
    path('shop', views.shop, name = "shop"),
    path('about', views.about, name = 'aboutus'),
    path('contact', views.contact, name = 'contactus'),
    path('shop/<int:cat_id>/', views.category, name = "category"),
    path('shop/<int:cat_id>/product/<int:prod_id>', views.product, name = "product"),
    path('cart', views.view_cart, name = "cart"),
    path('add/<int:product_id>/<int:qty>/', views.add_to_cart, name = "add_to_cart" ),
    path('remove/<int:cart_item_id>/', views.delete_from_cart, name = "delete_from_cart"),
    path('update/<int:cart_item_id>/<int:qty>/', views.update_cart, name = "update_cart"),
]