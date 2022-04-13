from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ProductHistory, Articles

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'favorites']


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['article', ]


class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHistory
        fields = ['article', 'name', 'old_price', 'final_price', 'brand',
                  'seller', 'add_date']
