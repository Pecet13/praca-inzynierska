from django.urls import path
from . import views

urlpatterns = [
    path('ai-users/', views.AIUserView.as_view(), name='ai-user-list'),
    path(
        'product-types/', views.ProductTypeListView.as_view(), name='product-type-list'
    ),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='product-detail'),
    path(
        'products/<int:pk>/review/',
        views.ComparisonListCreateView.as_view(),
        name='product-review',
    ),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('my-reviews/', views.ReviewListView.as_view(), name='my-reviews'),
    path('rankings/', views.RankingListView.as_view(), name='ranking-list'),
]
