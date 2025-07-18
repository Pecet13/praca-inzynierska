from django.test import TestCase
from django.contrib.auth.models import User
from ..models import ProductType, Product, Category, Comparison, Ranking

class RankingTestCase(TestCase):
    def setUp(self):
        pass

    def test_ranking_2_products_no_comparisons(self):
        pass

    def test_ranking_2_products_1_comparison(self):
        pass

    def test_ranking_2_products_1_comparison_draw(self):
        pass

    def test_ranking_2_products_2_comparisons(self):
        pass

    def test_ranking_2_products_2_comparisons_draw(self):
        pass

    def test_ranking_2_products_3_comparisons(self):
        pass

    def test_ranking_2_products_3_comparisons_draw(self):
        pass

    def test_ranking_3_products_normal(self):
        pass

    def test_ranking_3_products_transitive_closure(self):
        pass

    def test_ranking_4_products_normal(self):
        pass

    def test_ranking_4_products_transitive_closure(self):
        pass
