import pytest


class TestAuthAPI:
    @pytest.mark.django_db(transaction=True)
    def test_auth(self, client, user):
        response = client.post(
            '/api/auth/jwt/create/',
            data={'username': user.username, 'password': '1234567'}
        )

        assert response.status_code != 404, (
            'Страница `/api/auth/jwt/create/` '
            'не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 200, (
            'Страница `/api/auth/jwt/create/` '
            'работает не правильно'
        )

        auth_data = response.json()
        assert 'refresh' in auth_data and 'access' in auth_data, (
            'Проверьте, что при POST запросе `/api/auth/jwt/create/` '
            'возвращаете токен'
        )
