from datetime import date

import pytest

from ..models import ProductHistory


class TestProductsAPI:

    @pytest.mark.django_db(transaction=True)
    def test_products_not_found(self, client):
        response = client.get('/api/products/')

        assert response.status_code != 404, (
            'Страница `/api/products/` '
            'не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_products_not_auth(self, client, favorite_article):
        response = client.get('/api/products/')

        assert response.status_code == 401, (
            'Проверьте, что `/api/products/` '
            'не доступен для чтения неавторизованному пользователю'
        )
        assert response.status_code != 500, (
            'Проверьте, что `/api/products/` '
            'не вызывает ошибок на стороне сервера'
        )

    @pytest.mark.django_db(transaction=True)
    def test_products_auth_get(self, user, user_client, favorite_article,
                               product_history1):
        data = {}
        response = user_client.get('/api/products/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/products/` '
            'без article возвращаетсся статус 400'
        )

        data = {'article': 111}
        response = user_client.get('/api/products/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/products/` '
            'без from_date возвращаетсся статус 400'
        )

        data = {'article': 111, 'from_date': date.today()}
        response = user_client.get('/api/products/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/products/` '
            'без to_date возвращаетсся статус 400'
        )

        data = {'article': 111, 'from_date': date.today(),
                'to_date': date.today()}
        response = user_client.get('/api/products/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/products/` '
            'без interval возвращаетсся статус 400'
        )

        data = {'article': 111, 'from_date': date.today(),
                'to_date': date.today(), 'interval': 2}
        response = user_client.get('/api/products/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/products/` '
            'с не правильным параметром interval возвращаетсся статус 400'
        )

        data = {'article': 111, 'from_date': date.today(),
                'to_date': date.today(), 'interval': 1}
        response = user_client.get('/api/products/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/products/` '
            'с правильными параметрами возвращаетсся статус 200'
        )
        test_data = response.json()
        assert type(test_data) == dict, (
            'Проверьте, что при GET запросе на `/api/products/` '
            'возвращается словарь'
        )
        results = test_data['results']
        assert type(results) == list, (
            'Проверьте, что при GET запросе на `/api/products/` '
            'в поле results возвращается список'
        )

        assert len(results) == ProductHistory.objects.count(), (
            'Проверьте, что при GET запросе на `/api/products/` '
            'возвращается список с данными товаров'
        )

    @pytest.mark.django_db(transaction=True)
    def test_products_auth_post(self, user_client, user):
        data = {}
        response = user_client.post('/api/products/', data=data)
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе на `/api/products/` '
            'метод не разрешен'
        )

    @pytest.mark.django_db(transaction=True)
    def test_products_auth_delete(self, user_client, user):
        data = {}
        response = user_client.delete('/api/products/', data=data)
        assert response.status_code == 405, (
            'Проверьте, что при DELETE запросе на `/api/products/` '
            'метод не разрешен'
        )
