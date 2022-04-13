import pytest

from ..models import Articles, Favorites


class TestFavoritesAPI:

    @pytest.mark.django_db(transaction=True)
    def test_favorites_not_found(self, client):
        response = client.get('/api/favorites/')
        assert response.status_code != 404, (
                'Страница `/api/v1/posts/` '
                'не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorites_not_auth(self, client, favorite_article):
        response = client.get('/api/favorites/')

        assert response.status_code == 401, (
            'Проверьте, что `/api/favorites/` '
            'не доступен для чтения неавторизованному пользователю'
        )
        assert response.status_code != 500, (
            'Проверьте, что `/api/favorites/` '
            'не вызывает ошибок на стороне сервера'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorites_auth_get(self, user, user_client, favorite_article):
        response = user_client.get('/api/favorites/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/favorites/` '
            'с токеном авторизации возвращаетсся статус 200'
        )

        test_data = response.json()
        assert type(test_data) == dict, (
            'Проверьте, что при GET запросе на `/api/favorites/` '
            'возвращается словарь'
        )
        results = test_data['results']
        assert type(results) == list, (
            'Проверьте, что при GET запросе на `/api/favorites/` '
            'в поле results возвращается список'
        )

        assert len(results) == Favorites.objects.filter(user=user).count(), (
            'Проверьте, что при GET запросе на `/api/favorites/` '
            'возвращается только ваш список'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorites_auth_post(self, user_client, user, favorite_article):
        favorites_count = Favorites.objects.filter(user=user).count()
        articles_count = Articles.objects.count()

        data = {}
        response = user_client.post('/api/favorites/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/api/favorites/` '
            'с не правильными данными возвращается статус 400'
        )

        data = {'article': 333}
        response = user_client.post('/api/favorites/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/api/favorites/` '
            'с правильными данными возвращается статус 201'
        )

        test_data = response.json()

        msg_error = (
            'Проверьте, что при POST запросе на `/api/favorites/` '
            'возвращается словарь с сообщением об успешном добавлении'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('message') == 'Артикул добавлен', msg_error

        assert favorites_count + 1 == Favorites.objects.filter(
            user=user).count(), (
            'Проверьте, что при POST запросе на `/api/favorites/` '
            'в Favorites добавляются артикулы'
        )

        assert articles_count + 1 == Articles.objects.count(), (
            'Проверьте, что при POST запросе на `/api/favorites/` '
            'в Articles создаётся новый артикул'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorites_auth_delete(self, user_client, user, favorite_article):
        favorites_count = Favorites.objects.filter(user=user).count()
        articles_count = Articles.objects.count()

        data = {}
        response = user_client.delete('/api/favorites/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при DELETE запросе на `/api/favorites/` '
            'с без данных возвращается статус 400'
        )

        data = {'article': 333}
        response = user_client.delete('/api/favorites/', data=data)
        assert response.status_code == 404, (
            'Проверьте, что при DELETE запросе на `/api/favorites/` '
            'с не правильными данными возвращается статус 404'
        )

        data = {'article': 111}
        response = user_client.delete('/api/favorites/', data=data)
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе на `/api/favorites/` '
            'с правильными данными возвращается статус 204'
        )

        assert favorites_count - 1 == Favorites.objects.filter(
            user=user).count(), (
            'Проверьте, что при DELETE запросе на `/api/favorites/` '
            'в Favorites удаляется артикул'
        )

        assert articles_count == Articles.objects.count(), (
            'Проверьте, что при DELETE запросе на `/api/favorites/` '
            'в Articles ничего не меняется'
        )
