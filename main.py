import requests
import argparse
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(long_url, token):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "long_url": long_url
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(token, link):
    parsed_url = urlparse(link)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()["total_clicks"]


def is_bitlink(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    parsed_url= urlparse(link)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description = 'Этот проект сокращает ссылки через сайт bitly и выводит их сокращённую рабочую версию, а также показывает количество кликов по сокращенной ссылке.')
    parser.add_argument('link', type=str, help='Введите ссылку')
    args = parser.parse_args()
    try:
        if is_bitlink(bitly_token, args.link):
            print("Количество переходов по сылке: ", count_clicks(bitly_token, args.link))
        else:
            bitlink = shorten_link(args.link, bitly_token)
            print(bitlink)
    except requests.exceptions.HTTPError:
        print("Ссылка не правельная")

