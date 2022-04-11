from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class Products(models.Model):
    vendor_code = models.IntegerField('Артикул', unique=True)
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


class CustomUser(AbstractUser):
    products = models.ManyToManyField(Products)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


User = get_user_model()
