import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(long_url, headers):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {'long_url': long_url}
    response = requests.post(url, headers=headers, json=payload)
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
        description='Описание что делает программа'
    )
    parser.add_argument('name', help='Ваше имя')
    args = parser.parse_args()
    print(args.name)
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    args = parser.parse_args(long_url)
    parsed_url = urlparse(long_url)
    url_without_scheme = parsed_url.netloc + parsed_url.path
    headers = {"Authorization": f"Bearer {bitly_token}"}

    try:
        if is_bitlink(url_without_scheme, headers):
            print('', count_clicks(url_without_scheme, headers))
        else:
            print('', shorten_link(long_url, headers))
    except requests.exceptions.HTTPError as error:
        exit("Ошибка:  Неверная ссылка".format(error))
