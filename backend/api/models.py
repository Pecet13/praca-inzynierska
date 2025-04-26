from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product1 = models.ForeignKey(Product, related_name='product1', on_delete=models.CASCADE)
    product2 = models.ForeignKey(Product, related_name='product2', on_delete=models.CASCADE)
    result = models.CharField(max_length=100, choices=[('product1', 'Product 1'), ('product2', 'Product 2'), ('draw', 'Draw')], default='draw')
    user_created = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product1.name} vs {self.product2.name} - {self.category.name}, Result: {self.result}"
    

class Ranking(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.FloatField()
    rank = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.category.name}, Ranking: {self.rank}"
