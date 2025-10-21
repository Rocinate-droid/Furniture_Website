# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Room, Product, Categorie, Testimonial



class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'aboutus', 'contactus']  # These should be your URL names

    def location(self, item):
        return reverse(item)
    
class RoomPostSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Room.objects.all()
    
    def lastmod(self, obj):
        return obj.updated
    
class ProductPostSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.updated
    
class CategoriePostSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Categorie.objects.all()
    
    def lastmod(self, obj):
        return obj.updated
