from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='product-detail'),
    path('products/<int:pk>/review/', views.ComparisonListView.as_view(), name='product-review')
]
