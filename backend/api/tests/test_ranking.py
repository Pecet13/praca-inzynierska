from django.test import TestCase
from django.contrib.auth.models import User
from ..models import ProductType, Product, Category, Comparison, Ranking
from ..services import update_rankings


class RankingTestCase(TestCase):
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
        self.category = Category.objects.create(
            name="Test Category", product_type=self.product_type
        )

    def test_ranking_2_products_no_comparisons(self):
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 0.5"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 1, Score: 0.5"
        )

    def test_ranking_2_products_1_comparison(self):
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 1.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 2, Score: 0.0"
        )

    def test_ranking_2_products_1_comparison_draw(self):
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 0.5"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 1, Score: 0.5"
        )

    def test_ranking_2_products_2_comparisons(self):
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 1.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 2, Score: 0.0"
        )

    def test_ranking_2_products_2_comparisons_draw(self):
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Less",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 0.5"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 1, Score: 0.5"
        )

    def test_ranking_2_products_3_comparisons(self):
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Less",
        )
        self.comparison3 = Comparison.objects.create(
            user=self.user3,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Less",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 2, Score: 0.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 1, Score: 1.0"
        )

    def test_ranking_2_products_3_comparisons_draw(self):
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Less",
        )
        self.comparison3 = Comparison.objects.create(
            user=self.user3,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="Equal",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 0.5"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 1, Score: 0.5"
        )

    def test_ranking_3_products_normal(self):
        self.product3 = Product.objects.create(
            name="Test Product 3",
            product_type=self.product_type,
            description="Third test product",
            image_url="example.com/image3.jpg",
        )
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product3,
            result="More",
        )
        self.comparison3 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product2,
            product2=self.product3,
            result="Equal",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        ranking_p3 = Ranking.objects.get(product=self.product3)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 2.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 2, Score: 0.5"
        )
        self.assertEqual(
            str(ranking_p3), "Test Product 3 - Test Category, Rank: 2, Score: 0.5"
        )

    def test_ranking_3_products_transitive_closure(self):
        self.product3 = Product.objects.create(
            name="Test Product 3",
            product_type=self.product_type,
            description="Third test product",
            image_url="example.com/image3.jpg",
        )
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product2,
            product2=self.product3,
            result="More",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        ranking_p3 = Ranking.objects.get(product=self.product3)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 2.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 2, Score: 1.0"
        )
        self.assertEqual(
            str(ranking_p3), "Test Product 3 - Test Category, Rank: 3, Score: 0.0"
        )

    def test_ranking_4_products_normal(self):
        self.product3 = Product.objects.create(
            name="Test Product 3",
            product_type=self.product_type,
            description="Third test product",
            image_url="example.com/image3.jpg",
        )
        self.product4 = Product.objects.create(
            name="Test Product 4",
            product_type=self.product_type,
            description="Fourth test product",
            image_url="example.com/image4.jpg",
        )
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product3,
            result="More",
        )
        self.comparison3 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product3,
            product2=self.product4,
            result="Equal",
        )
        self.comparison4 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product2,
            product2=self.product4,
            result="Less",
        )
        self.comparison5 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product3,
            product2=self.product2,
            result="More",
        )
        self.comparison6 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product1,
            product2=self.product4,
            result="More",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        ranking_p3 = Ranking.objects.get(product=self.product3)
        ranking_p4 = Ranking.objects.get(product=self.product4)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 3.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 4, Score: 0.0"
        )
        self.assertEqual(
            str(ranking_p3), "Test Product 3 - Test Category, Rank: 2, Score: 1.5"
        )
        self.assertEqual(
            str(ranking_p4), "Test Product 4 - Test Category, Rank: 2, Score: 1.5"
        )

    def test_ranking_4_products_transitive_closure(self):
        self.product3 = Product.objects.create(
            name="Test Product 3",
            product_type=self.product_type,
            description="Third test product",
            image_url="example.com/image3.jpg",
        )
        self.product4 = Product.objects.create(
            name="Test Product 4",
            product_type=self.product_type,
            description="Fourth test product",
            image_url="example.com/image4.jpg",
        )
        self.comparison1 = Comparison.objects.create(
            user=self.user1,
            category=self.category,
            product1=self.product1,
            product2=self.product2,
            result="More",
        )
        self.comparison2 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product2,
            product2=self.product3,
            result="More",
        )
        self.comparison3 = Comparison.objects.create(
            user=self.user2,
            category=self.category,
            product1=self.product3,
            product2=self.product4,
            result="More",
        )
        update_rankings()
        ranking_p1 = Ranking.objects.get(product=self.product1)
        ranking_p2 = Ranking.objects.get(product=self.product2)
        ranking_p3 = Ranking.objects.get(product=self.product3)
        ranking_p4 = Ranking.objects.get(product=self.product4)
        self.assertEqual(
            str(ranking_p1), "Test Product 1 - Test Category, Rank: 1, Score: 3.0"
        )
        self.assertEqual(
            str(ranking_p2), "Test Product 2 - Test Category, Rank: 2, Score: 2.0"
        )
        self.assertEqual(
            str(ranking_p3), "Test Product 3 - Test Category, Rank: 3, Score: 1.0"
        )
        self.assertEqual(
            str(ranking_p4), "Test Product 4 - Test Category, Rank: 4, Score: 0.0"
        )
