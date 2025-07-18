from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import ProductType, Category


class CategoryTestCase(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(name="Test Type")
        self.category = Category.objects.create(
            name="Test Category", product_type=self.product_type
        )

    def test_category_fields(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_category_no_name(self):
        self.assertRaises(
            IntegrityError,
            Category.objects.create,
            name=None,
            product_type=self.product_type,
        )

    def test_category_no_product_type(self):
        self.assertRaises(
            IntegrityError,
            Category.objects.create,
            name="Test Category 2",
            product_type=None,
        )
