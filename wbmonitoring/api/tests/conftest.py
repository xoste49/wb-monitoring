import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser', password='1234567')


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser2', password='1234567')


@pytest.fixture
def token(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    token = RefreshToken.for_user(user)
    print('token.access_token:', token.access_token)
    return token.access_token


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def article1():
    from ..models import Articles
    return Articles.objects.create(article=111)


@pytest.fixture
def article2():
    from ..models import Articles
    return Articles.objects.create(article=222)


@pytest.fixture
def favorite_article(user, article1):
    from ..models import Favorites
    return Favorites.objects.create(user=user, article=article1)


@pytest.fixture
def product_history1(article1):
    from ..models import ProductHistory
    return ProductHistory.objects.create(
        article=article1, name='Имя 1',
        old_price=111, final_price=11,
        brand='Брэнд 1', seller='Поставщик 1'
    )


@pytest.fixture
def product_history2(article2):
    from ..models import ProductHistory
    return ProductHistory.objects.create(
        article=article2, name='Имя 2',
        old_price=222, final_price=22,
        brand='Брэнд 2', seller='Поставщик 2'
    )
