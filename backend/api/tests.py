from django.test import TestCase
from .models import ProductType, Product, Category, Comparison, Ranking


class ProductTypeTestCase(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(name="Test Type")

    def test_product_type_str(self):
        self.assertEqual(str(self.product_type), "Test Type")
