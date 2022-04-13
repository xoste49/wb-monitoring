import datetime


from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, DateTimeField
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly, IsAdminUser

from .models import Articles, ProductHistory
from .serializers import UserSerializer, ArticlesSerializer, ProductHistorySerializer

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

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



class ProductHistoryViewSet(viewsets.ReadOnlyModelViewSet):
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
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        interval = int(interval)
        if interval not in (1, 30, 60):
            raise ValidationError(
                'error: interval должен быть равен 1, 12, 24 часа',
                status.HTTP_400_BAD_REQUEST
            )
        queryset = Articles.objects.get(article=article)
        queryset = queryset.history.filter(add_date__range=(from_date, to_date))
        if interval == 1:
            minutes = [x for x in range(0, 24)]
            return queryset.filter(add_date__hour__in=minutes)
        elif interval == 12:
            return queryset.filter(add_date__hour__in=(0, 30))
        elif interval == 24:
            return queryset.filter(add_date__hour=0)
