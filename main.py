import argparse
import logging
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(long_url, headers):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {'long_url': long_url}
    response = requests.post(url, headers=headers, json=payload)
    headers = {"Authorization": f"Bearer {bitly_token}"}
    response.raise_for_status()
    return response.json()['link']


def count_clicks(bitlink, headers):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(bitlink, headers):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Данная программа сокращает ссылки и показывает количество кликов по ним'
    )
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    parsed_url = urlparse(args.link)
    url_without_scheme = f'{parsed_url.netloc}{parsed_url.path}'

    try:
        if is_bitlink(url_without_scheme, headers):
            print('', count_clicks(url_without_scheme, headers))
        else:
            print('', shorten_link(args.link, headers))
    except requests.exceptions.HTTPError as error:
       logging.error("Ошибка:  Неверная ссылка".format(error))
