from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
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
