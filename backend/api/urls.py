from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='product-detail'),
    path('products/<int:pk>/review/', views.ComparisonListCreateView.as_view(), name='product-review'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('my-reviews/', views.ReviewListView.as_view(), name='my-reviews')
]
