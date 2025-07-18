from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import ProductType


class ProductTypeTestCase(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(name="Test Type")

    def test_product_type_fields(self):
        self.assertEqual(str(self.product_type), "Test Type")

    def test_product_type_no_name(self):
        self.assertRaises(IntegrityError, ProductType.objects.create, name=None)
