from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import ProductType, Product, Category, Comparison


class ComparisonTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.user3 = User.objects.create_user(username="user3", password="password")
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
            image_url="example.com/image2.jpg",
        )
        self.product3 = Product.objects.create(
            name="Test Product 3",
            product_type=self.product_type,
            description="Third test product",
            image_url="example.com/image3.jpg",
        )
        self.category = Category.objects.create(
            name="Test Category", product_type=self.product_type
        )
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product3,
            product2=self.product2,
            result="Less",
        )
        self.comparison3 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )

    def test_comparison_fields(self):
        self.assertEqual(
            str(self.comparison1),
            "Comparison in category: Test Category, Test Product 1 is More than Test Product 2",
        )
        self.assertEqual(self.comparison1.user, self.user1)
        self.assertEqual(
            str(self.comparison2),
            "Comparison in category: Test Category, Test Product 3 is Less than Test Product 2",
        )
        self.assertEqual(self.comparison2.user, self.user1)
        self.assertEqual(
            str(self.comparison3),
            "Comparison in category: Test Category, Test Product 1 and Test Product 2 are Equal",
        )
        self.assertEqual(self.comparison3.user, self.user2)

    def test_comparison_missing_user(self):
        self.assertRaises(
            IntegrityError,
            Comparison.objects.create,
            user=None,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )

    def test_comparison_missing_category(self):
        self.assertRaises(
            IntegrityError,
            Comparison.objects.create,
            user=self.user3,
            category=None,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )

    def test_comparison_missing_product1(self):
        self.assertRaises(
            IntegrityError,
            Comparison.objects.create,
            user=self.user3,
            category=self.category,
            product1=None,
            product2=self.product2,
            result="Equal",
        )

    def test_comparison_missing_product2(self):
        self.assertRaises(
            IntegrityError,
            Comparison.objects.create,
            user=self.user3,
            category=self.category,
            product1=self.product1,
            product2=None,
            result="Equal",
        )

    def test_comparison_missing_result(self):
        self.assertRaises(
            IntegrityError,
            Comparison.objects.create,
            user=self.user3,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result=None,
        )

    def test_unique_comparison(self):
        self.assertRaises(
            IntegrityError,
            Comparison.objects.create,
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )
