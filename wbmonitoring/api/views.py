import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Articles, Favorites
from .serializers import ProductHistorySerializer, CreateFavoriteSerializer, \
    GetFavoriteSerializer

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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Артикул добавлен'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        if not request.data.get('article'):
            raise ValidationError('Не передан параметр article')
        article_value = request.data.get('article')
        if not article_value.isdigit():
            raise ValidationError('Артикул должен состоять только из цифр')
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

    def get_queryset(self):
        article = self.request.query_params.get('article')
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        interval = self.request.query_params.get('interval')
        if article is None:
            raise ValidationError(
                'error: не передан параметр article',
                status.HTTP_400_BAD_REQUEST
            )
        if from_date is None:
            raise ValidationError(
                'error: не передан параметр from_date',
                status.HTTP_400_BAD_REQUEST
            )
        if to_date is None:
            raise ValidationError(
                'error: не передан параметр to_date',
                status.HTTP_400_BAD_REQUEST
            )
        if interval is None:
            raise ValidationError(
                'error: не передан параметр interval',
                status.HTTP_400_BAD_REQUEST
            )
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        from_date = datetime.datetime.combine(from_date, datetime.time.min)
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.combine(to_date, datetime.time.max)
        interval = int(interval)
        if interval not in (1, 30, 60):
            raise ValidationError(
                'error: interval должен быть равен 1, 12, 24 часа',
                status.HTTP_400_BAD_REQUEST
            )
        queryset = Articles.objects.get(article=article)
        queryset = queryset.history.filter(
            add_date__range=(from_date, to_date))
        if interval == 1:
            minutes = [x for x in range(0, 24)]
            return queryset.filter(add_date__hour__in=minutes)
        elif interval == 12:
            return queryset.filter(add_date__hour__in=(0, 30))
        elif interval == 24:
            return queryset.filter(add_date__hour=0)
