from django.contrib import admin
from .models import ProductType, Product, Category

admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Category)
