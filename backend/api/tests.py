from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
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
            image_url="example.com/image3.jpg",
        )

    def test_product_no_description(self):
        self.assertRaises(
            IntegrityError,
            Product.objects.create,
            name="Test Product 3",
            product_type=self.product_type,
            description=None,
            image_url="example.com/image3.jpg",
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


class ComparisonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product_type = ProductType.objects.create(name="Test Type")
        self.product_type2 = ProductType.objects.create(name="Test Type 2")
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
        self.product4 = Product.objects.create(
            name="Test Product 3",
            product_type=self.product_type2,
            description="Fourth test product",
            image_url="example.com/image4.jpg",
        )
        self.category = Category.objects.create(
            name="Test Category", product_type=self.product_type
        )
        self.category2 = Category.objects.create(
            name="Test Category", product_type=self.product_type2
        )
        self.comparison1 = Comparison.objects.create(
            user=self.user,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user,
            category=self.category,
            product1=self.product3,
            product2=self.product2,
            result="Less",
        )

    def test_comparison_same_product(self):
        url = reverse("product-review", kwargs={"pk": self.product1.id})
        payload = [
            {
                "category": self.category.id,
                "product2": self.product1.id,
                "result": "Equal",
            }
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Cannot compare Test Product 1 with itself in category Test Category.",
            response.data[0]
        )

    def test_comparison_same_pair(self):
        url = reverse("product-review", kwargs={"pk": self.product1.id})
        payload = [
            {
                "category": self.category.id,
                "product2": self.product2.id,
                "result": "Equal",
            },
            {
                "category": self.category.id,
                "product2": self.product2.id,
                "result": "More",
            }
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Duplicate comparison with Test Product 2 in category Test Category.",
            response.data[0]
        )

    def test_comparison_same_pair_reverse(self):
        pass

    def test_comparison_product_different_product_type(self):
        pass

    def test_comparison_category_different_product_type(self):
        pass

    def test_comparison_cycle_detection(self):
        pass
