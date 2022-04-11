from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class Articles(models.Model):
    article = models.IntegerField('Артикул', unique=True)
    #last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Артикул'
        verbose_name_plural = 'Артикулы'
        ordering = ['article']

    def __str__(self):
        return str(self.article)


class ProductHistory(models.Model):
    article = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        verbose_name="Артикул",
        related_name="history",
    )
    name = models.CharField('Наименование', max_length=500)
    price = models.DecimalField(
        'Цена без скидки',
        max_digits=10,
        decimal_places=2
    )
    discount_price = models.DecimalField(
        'Цена со скидкой',
        max_digits=10,
        decimal_places=2
    )
    brand = models.CharField('Бренд', max_length=100)
    seller = models.CharField('Поставщик', max_length=100)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Артикул'
        verbose_name_plural = 'Артикулы'
        ordering = ['-add_date']

    def __str__(self):
        return self.code


class CustomUser(AbstractUser):
    favorites = models.ManyToManyField(Articles)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


User = get_user_model()
