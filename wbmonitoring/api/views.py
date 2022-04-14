from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ProductHistoryFilterBackend
from .models import Articles, Favorites
from .serializers import (CreateFavoriteSerializer, GetFavoriteSerializer,
                          ProductHistorySerializer)
from .tasks import parse_wb_article
from .validators import article_isdigit_validator

User = get_user_model()


class FavoritesViewSet(viewsets.ModelViewSet):
    """
    Артикулы пользователей

    GET - Получаем список добавленных артикулов пользователя
    POST - Добавляем артикул в список пользователя
             если артикула нет в базе артикулов то добавляем и туда
    DELETE - Удаляем артикул из списка пользователя
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create',):
            return CreateFavoriteSerializer
        else:
            return GetFavoriteSerializer

    def get_queryset(self):
        return self.request.user.favorite.all().order_by('article')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = Favorites.objects.filter(
            user=self.request.user,
            article__article=request.data.get('article'))
        if obj.exists():
            raise ValidationError(
                {'error': 'Артикул уже в избранном'},
                status.HTTP_400_BAD_REQUEST
            )
        if not Articles.objects.filter(
                article=request.data.get('article')).exists():
            # Если артикула нет в базе, то сохраняем и ставим задачу спарсить
            self.perform_create(serializer)
            parse_wb_article.delay(request.data.get('article'))
        else:
            # Иначе только сохраняем в базе
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Артикул добавлен'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        if not request.data.get('article'):
            raise ValidationError('Не передан параметр article')
        article_value = request.data.get('article')
        article_isdigit_validator(article_value)
        article = get_object_or_404(Articles, article=article_value)
        obj = Favorites.objects.filter(
            user=self.request.user,
            article=article
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Артикула нету в избранном"},
                            status=status.HTTP_400_BAD_REQUEST)


class ProductHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    История карточек товаров с фильтрацией
    """
    serializer_class = ProductHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [ProductHistoryFilterBackend]
