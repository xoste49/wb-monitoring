# Wildberries Monitoring

Автоматически отслеживать динамику изменения параметров карточки товара на
маркетплейсе Wildberries (далее Карточка), получать по запросу статистическую
информацию о состоянии параметров Карточки в заданном диапазоне дат с
заданным временным интервалом (не чаще 1 записи в час).  

## .env
```
DEBUG=0 # указываем, включение или отключение отладки
SECRET_KEY=topsecretcode # Секретный ключ в настройках Django, сгенерировать можно здесь https://djecrety.ir/
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] # Список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django.
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=wbmonitoring # имя базы данных
SQL_USER=postgres # логин для подключения к базе данных
SQL_PASSWORD=postgres # пароль для подключения к БД (установите свой)
SQL_HOST=db
SQL_PORT=5432
CELERY_BROKER_URL=redis://redis:6379
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
POSTGRES_DB=wbmonitoring # имя базы данных
```

## Quick Start
```shell
git clone https://github.com/xoste49/wb-monitoring
cd wb-monitoring
touch .env
nano .env # заполняем по шаблоны выше
sudo docker-compose up -d
# Создание миграций
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
# Перезапускаем контейнеры
sudo docker-compose restart
# Создаём администратора
sudo docker exec -it wb-monitoring_web_1 python manage.py createsuperuser  
```

## URLs
```
/api/auth/users/ POST - Зарегистрироваться
/api/auth/jwt/create/ POST - Создать токен
/api/favorites/ GET - Получаем список добавленных артикулов пользователя
/api/favorites/ POST - Добавляем артикул в список пользователя если артикула нет в базе артикулов то добавляем и туда
Обязательный параметр: article - артикул товара
/api/favorites/ DELETE - Удаляем артикул из списка пользователя
Обязательный параметр: article - артикул товара
/api/products/ GET - Просмотр Карточки товара с фильтрацией артикул товара, дату начала периода, дату окончания периода, интервал (на выбор 1 час, 12 часов, 24 часа)
Обязательные параметры: 
article - артикул товара
from_date - дату начала периода в формате (2022-03-22)
to_date - дату окончания периода в формате (2022-03-22)
interval - интервал (на выбор 1 час, 12 часов, 24 часа)
```