from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Articles, Favorites, ProductHistory

User = get_user_model()


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['article', ]


class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHistory
        fields = ['article', 'name', 'old_price', 'final_price', 'brand',
                  'seller', 'add_date']


class GetFavoriteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return ArticlesSerializer(instance.article).data['article']

    class Meta:
        fields = ('article',)
        model = Favorites
        read_only_fields = ('user', 'article')


class CreateFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    article = serializers.CharField()

    def validate_article(self, article):
        if not article.isdigit():
            raise ValidationError('Артикул должен состоять только из цифр')
        return article

    def create(self, validated_data):
        article = validated_data.pop('article')
        article_instance, created = Articles.objects.get_or_create(
            article=article
        )
        return Favorites.objects.create(
            **validated_data,
            article=article_instance
        )

    class Meta:
        fields = ('user', 'article')
        model = Favorites
        read_only_fields = ('user', 'article')
