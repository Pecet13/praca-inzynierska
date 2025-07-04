from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ProductType, Product, Category, Comparison, Ranking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_type', 'description', 'image_url']
        extra_kwargs = {'image_url': {'required': False}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_type']


class ComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = ['id', 'user', 'category', 'product1', 'product2', 'result']
        extra_kwargs = {'user': {'read_only': True}, 'product1': {'read_only': True}}


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ['id', 'category', 'product', 'score', 'rank']
        extra_kwargs = {'category': {'read_only': True}, 'product': {'read_only': True}}
        depth = 1
