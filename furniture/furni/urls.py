from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('shop', views.shop, name = "shop"),
    path('about', views.about, name = 'aboutus'),
    path('contact', views.contact, name = 'contactus'),
    path('services', views.services, name = 'services'),
    path('shop/<int:cat_id>/', views.category, name = "category"),
    path('leadership', views.leaders, name="leaders"),
    path('carrers',views.carrers, name="carrers"),
    path('register',views.registerpage, name="registerpage"),
    path('login',views.loginpage, name="loginpage"),
    path('logout',views.logoutrequest, name="logoutpage"),
    #path('profile',views.profilepage, name="profilepage"),
    path('shop/<int:cat_id>/product/<int:prod_id>', views.product, name = "product"),
    path('cart', views.view_cart, name = "cart"),
    path('add/<int:product_id>/<int:qty>/', views.add_to_cart, name = "add_to_cart" ),
    path('buy/<int:product_id>/<int:qty>/', views.buynow, name = "buy_now"),
    path('remove/<int:cart_item_id>/', views.delete_from_cart, name = "delete_from_cart"),
    path('update/<int:cart_item_id>/<int:qty>/', views.update_cart, name = "update_cart"),
    path('checkout', views.checkout, name = 'checkout'),
]