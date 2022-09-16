import argparse
import logging
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(long_url, bitly_token):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {'long_url': long_url}
    headers = {"Authorization": f"Bearer {bitly_token}"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(bitlink, bitly_token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {"Authorization": f"Bearer {bitly_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(bitlink, bitly_token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {"Authorization": f"Bearer {bitly_token}"}
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
        if is_bitlink(url_without_scheme, bitly_token):
            print('', count_clicks(url_without_scheme, bitly_token))
        else:
            print('', shorten_link(args.link, bitly_token))
    except requests.exceptions.HTTPError:
       logging.exception("Ошибка:  Неверная ссылка")
