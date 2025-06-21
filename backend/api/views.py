from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
        product1 = self.kwargs['pk']
        return Comparison.objects.filter(user=self.request.user, product1=product1)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Remove existing comparisons
        product1 = Product.objects.get(pk=kwargs['pk'])
        Comparison.objects.filter(user=request.user, product1=product1).delete()

        # Validate and create new comparisons
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)

        for item in serializer.validated_data:
            category = item['category']
            product2 = item['product2']
            if Comparison.objects.filter(user=request.user, category=category, product1=product2, product2=product1).exists():
                raise ValidationError(f'You have already compared {product1.name} and {product2.name} in category {category.name}.')
            if item['result'] == 'equal':
                continue
            if item['result'] == 'more':
                src_product, dst_product = product2, product1
            else:
                src_product, dst_product = product1, product2
            if self.check_cycle(category, src_product, dst_product):
                raise ValidationError(f'Cycle detected between {product1.name} and {product2.name} in category {category.name}.')

        instances = []
        for item in serializer.validated_data:
            instances.append(
                Comparison.objects.create(
                    user=request.user,
                    category=item['category'],
                    product1=product1,
                    product2=item['product2'],
                    result=item['result'],
                    user_created=True
                )
            )
        
        # Serialize the created comparisons
        out = ComparisonSerializer(instances, many=True)
        return Response(out.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        Comparison.objects.filter(user=request.user, product1=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_cycle(self, category, src_product, dest_product):
        pass


class ReviewListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comparisons = Comparison.objects.filter(user=self.request.user, user_created=True)
        product_ids = comparisons.values_list('product1', flat=True).distinct()
        return Product.objects.filter(id__in=product_ids)
    