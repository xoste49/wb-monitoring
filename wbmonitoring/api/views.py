from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Articles, ProductHistory
from .serializers import UserSerializer, ArticlesSerializer, \
    ProductHistorySerializer

User = get_user_model()

"""
Я, как пользователь, хочу зарегистрироваться в сервисе, указать логин, пароль и
email.
Я, как пользователь, хочу редактировать список артикулов товаров, изменения в
которых мне нужно отслеживать.
"""
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorites(self, request):
        if self.request.method == 'GET':
            queryset = self.request.user.favorites.all()
            context = self.get_serializer_context()
            page = self.paginate_queryset(queryset.order_by('article'))
            serializer = ArticlesSerializer(
                page,
                context=context,
                many=True
            )
            return self.get_paginated_response(serializer.data)
        elif self.request.method == 'POST':
            # TODO: Проверкана integer
            # TODO: Перенести в отдельный файл валидаций
            if not request.data.get('article'):
                raise ValidationError(
                    {'errors': 'Не передан параметр article'},
                    status.HTTP_400_BAD_REQUEST
                )
            if self.request.user.favorites.filter(article=request.data.get('article')).exists():
                raise ValidationError(
                    {'errors': 'Артикул уже добавлен в избранные'},
                    status.HTTP_400_BAD_REQUEST
                )
            serializer = ArticlesSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                serializer.save()
                self.request.user.favorites.add(serializer.instance)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                article = Articles.objects.get(article=request.data.get('article'))
                self.request.user.favorites.add(article)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        elif self.request.method == 'DELETE':
            if not request.data.get('article'):
                raise ValidationError(
                    {'errors': 'Не передан параметр article'},
                    status.HTTP_400_BAD_REQUEST
                )
            if self.request.user.favorites.filter(article=request.data.get('article')).exists():
                article = Articles.objects.get(
                    article=request.data.get('article'))
                self.request.user.favorites.remove(article)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError(
                    {'errors': 'Артикул уже удален'},
                    status.HTTP_400_BAD_REQUEST
                )
        return Response('error')



"""
Я, как пользователь, хочу указать артикул товара, дату начала периода, дату
окончания периода, интервал (на выбор 1 час, 12 часов, 24 часа) и получить в
соответствии с заданными параметрами историческую информацию о параметрах
Карточки.
"""
class ProductHistoryViewSet(viewsets.ModelViewSet):
    queryset = ProductHistory.objects.all()
    serializer_class = ProductHistorySerializer
    permission_classes = [IsAuthenticated]
