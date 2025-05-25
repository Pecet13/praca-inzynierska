from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer, CategorySerializer, ComparisonSerializer
from .models import Product, Category, Comparison


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ComparisonListCreateView(generics.ListCreateAPIView):
    serializer_class = ComparisonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product1 = self.kwargs['pk']
        return Comparison.objects.filter(user=user, product1=product1)
    
    def perform_create(self, serializer):
        product1 = Product.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, product1=product1, user_created=True)

    def delete(self, request, pk):
        Comparison.objects.filter(user=request.user, product1=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comparisons = Comparison.objects.filter(user=self.request.user, user_created=True)
        product_ids = comparisons.values_list('product1', flat=True).distinct()
        return Product.objects.filter(id__in=product_ids)
    