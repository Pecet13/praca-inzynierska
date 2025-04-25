from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Category, Comparison, Ranking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image_url']
        extra_kwargs = {'image_url': {'required': False}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = ['id', 'user', 'category', 'product1', 'product2', 'result', 'user_created']
        extra_kwargs = {'user': {'read_only': True}}
        depth = 1


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ['id', 'category', 'product', 'score', 'rank']
        extra_kwargs = {'category': {'read_only': True}, 'product': {'read_only': True}}
        depth = 1
