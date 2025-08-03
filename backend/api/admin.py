from django.contrib import admin
from .models import ProductType, Product, Category, Comparison, Ranking

admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comparison)
admin.site.register(Ranking)
