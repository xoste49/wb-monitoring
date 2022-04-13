import traceback
from datetime import datetime

from celery import shared_task

from .models import Articles, ProductHistory
from .parsers import wb as parser_wb


@shared_task
def parse_wb():
    try:
        datetime_parse = datetime.now()
        for article in Articles.objects.all():
            try:
                product = parser_wb(article)
                if 'error' in product.keys():
                    print('error:', product['error'])
                    continue
                ProductHistory.objects.create(
                    article=article,
                    name=product['name'],
                    old_price=product['old_price'],
                    final_price=product['final_price'],
                    brand=product['brand'],
                    seller=product['seller'],
                    add_date=datetime_parse
                )
            except Exception as e:
                print('Ошибка!', str(e), 'При парсинге артикула:', article)
                print(traceback.format_exc())
    except Exception as e:
        print('Ошибка!', str(e))
        print(traceback.format_exc())
