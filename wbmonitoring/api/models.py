from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class Articles(models.Model):
    """
    Хранит в себе все артикулы
    """
    article = models.IntegerField('Артикул', unique=True)
    #last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Артикул'
        verbose_name_plural = 'Артикулы'
        ordering = ['article']

    def __str__(self):
        return str(self.article)


class ProductHistory(models.Model):
    """
    История карточек товаров
    """
    article = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        verbose_name="Артикул",
        related_name="history",
    )
    name = models.CharField('Наименование', max_length=500)
    old_price = models.DecimalField(
        'Цена без скидки',
        max_digits=10,
        decimal_places=2
    )
    final_price = models.DecimalField(
        'Цена со скидкой',
        max_digits=10,
        decimal_places=2
    )
    brand = models.CharField('Бренд', max_length=100)
    seller = models.CharField('Поставщик', max_length=100)
    add_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'История Товара'
        verbose_name_plural = 'Истории Товаров'
        ordering = ['-add_date']

    def __str__(self):
        return f'{str(self.article)} | {str(self.add_date)}'


class CustomUser(AbstractUser):
    """
    Пользователь с добавленным полем избранных артикулов
    """
    favorites = models.ManyToManyField(Articles)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


User = get_user_model()
