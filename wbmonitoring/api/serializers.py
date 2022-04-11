from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ProductHistory, Articles

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'favorites']


class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articles
        fields = ['article', ]


class ProductHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductHistory
        fields = ['number', 'name', 'price', 'discount_price', 'brand',
                  'seller', 'add_date']
