from django.test import TestCase
from django.db.utils import IntegrityError
from .models import ProductType, Product, Category, Comparison, Ranking


class ProductTypeTestCase(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(name="Test Type")

    def test_product_type_fields(self):
        self.assertEqual(str(self.product_type), "Test Type")

    def test_product_type_no_name(self):
        self.assertRaises(IntegrityError, ProductType.objects.create, name=None)


class ProductTestCase(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(name="Test Type")
        self.product1 = Product.objects.create(
            name="Test Product 1",
            product_type=self.product_type,
            description="First test product",
            image_url="example.com/image1.jpg",
        )
        self.product2 = Product.objects.create(
            name="Test Product 2",
            product_type=self.product_type,
            description="Second test product",
            image_url=None,
        )

    def test_product_fields(self):
        self.assertEqual(str(self.product1), "Test Product 1")
        self.assertEqual(self.product1.product_type, self.product_type)
        self.assertEqual(str(self.product1.description), "First test product")
        self.assertEqual(str(self.product1.image_url), "example.com/image1.jpg")
        self.assertEqual(str(self.product2), "Test Product 2")
        self.assertEqual(self.product2.product_type, self.product_type)
        self.assertEqual(str(self.product2.description), "Second test product")
        self.assertEqual(self.product2.image_url, None)

    def test_product_no_name(self):
        self.assertRaises(
            IntegrityError,
            Product.objects.create,
            name=None,
            product_type=self.product_type,
            description="Third test product",
            image_url="example.com/image3.jpg",
        )

    def test_product_no_product_type(self):
        self.assertRaises(
            IntegrityError,
            Product.objects.create,
            name="Test Product 3",
            product_type=None,
            description="First test product",
            image_url="example.com/image1.jpg",
        )

    def test_product_no_description(self):
        self.assertRaises(
            IntegrityError,
            Product.objects.create,
            name="Test Product 3",
            product_type=self.product_type,
            description=None,
            image_url="example.com/image1.jpg",
        )


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
