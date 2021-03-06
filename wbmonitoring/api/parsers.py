import json

import requests


def wb(article):
    """
    Парсер данных с сайта Wildberries
    :param article: Артикул товара
    :return: Словарь с дынными или с ошибкой
    """
    r_specification = requests.get(
        f'https://wbx-content-v2.wbstatic.net/ru/{article}.json'
    )
    if r_specification.status_code != 200:
        return {'error': ''}
    response_specification = json.loads(r_specification.text)
    brand = response_specification['selling']['brand_name']
    name = response_specification['imt_name']

    r_price = requests.get(
        'https://wbxcatalog-ru.wildberries.ru/nm-2-card/'
        f'catalog?locale=ru&lang=ru&curr=rub&nm={article}'
    )
    if r_price.status_code != 200:
        return {'error': ''}
    response_price = json.loads(r_price.text)
    products = response_price['data']['products']
    if len(products) == 0:
        return {'error': f'Товар с артикулом {article} отсутствует'}
    product = products[0]
    final_price = int(product['salePriceU'])/100
    old_price = int(product['priceU'])/100

    r_seller = requests.get(
        f'https://wbx-content-v2.wbstatic.net/sellers/{article}.json'
    )
    if r_seller.status_code != 200:
        return {'error': ''}
    response_seller = json.loads(r_seller.text)
    seller = response_seller['supplierName']
    return {
        'brand': brand,
        'name': name,
        'final_price': final_price,
        'old_price': old_price,
        'seller': seller,
    }
