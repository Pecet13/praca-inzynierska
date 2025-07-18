from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import ProductType, Product, Category, Comparison


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
            name="Test Product 4",
            product_type=self.product_type2,
            description="Fourth test product",
            image_url="example.com/image4.jpg",
        )
        self.category = Category.objects.create(
            name="Test Category", product_type=self.product_type
        )
        self.category2 = Category.objects.create(
            name="Test Category 2", product_type=self.product_type2
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
            response.data[0],
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
            },
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Duplicate comparison with Test Product 2 in category Test Category.",
            response.data[0],
        )

    def test_comparison_same_pair_reverse(self):
        url = reverse("product-review", kwargs={"pk": self.product2.id})
        payload = [
            {
                "category": self.category.id,
                "product2": self.product1.id,
                "result": "Equal",
            },
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "You have already compared Test Product 2 and Test Product 1 in category Test Category.",
            response.data[0],
        )

    def test_comparison_product_different_product_type(self):
        url = reverse("product-review", kwargs={"pk": self.product1.id})
        payload = [
            {
                "category": self.category.id,
                "product2": self.product4.id,
                "result": "Equal",
            },
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Product Test Product 4 does not belong to the same product type as Test Product 1.",
            response.data[0],
        )

    def test_comparison_category_different_product_type(self):
        url = reverse("product-review", kwargs={"pk": self.product1.id})
        payload = [
            {
                "category": self.category2.id,
                "product2": self.product2.id,
                "result": "Equal",
            },
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Category Test Category 2 does not belong to the same product type as Test Product 1.",
            response.data[0],
        )

    def test_comparison_cycle_detection(self):
        url = reverse("product-review", kwargs={"pk": self.product1.id})
        payload = [
            {
                "category": self.category.id,
                "product2": self.product3.id,
                "result": "Less",
            },
        ]
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Comparison between Test Product 1 and Test Product 3 in category Test Category contradicts with the data you provided before.",
            response.data[0],
        )
