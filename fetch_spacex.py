import requests
import logging
import http.client as httplib
import os
import pathlib
import random
from urllib.parse import urlparse


def fetch_spacex():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    httplib.HTTPConnection.debuglevel = 0  # 1 -включает
    logging.basicConfig(filename='insta.log', level=logging.DEBUG, format=log_format, filemode='w')
    logger = logging.getLogger("requests.packages.urllib3")
    logger.info(f'START {fetch_spacex.__name__}')

    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, 'images')
    image_name = 'space'
    spacex_api = 'https://api.spacexdata.com/v3/launches'
    flight_mode = 'latest'
    url_tuple = urlparse(spacex_api)
    headers = {
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    }
    headers['Host'] = url_tuple[1]
    pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)
    try:
        resp = requests.get(spacex_api, headers=headers)
        logger.info(f'Результат ссылки {spacex_api} на существование:{resp.status_code}')
        if not resp.ok:
            return exit(1)
        flights_with_links = {flight.get('flight_number'): flight['links'].get('flickr_images')
                              for flight in resp.json() if len(flight['links'].get('flickr_images')) > 0}
        flight_with_pics = {}
        if flight_mode == 'random':
            flight_with_pics = random.choice(flights_with_links)
        elif flight_mode == 'latest':
            flight_with_pics = flights_with_links.get(max(flights_with_links.keys()))
        for image_enum, link in enumerate(flight_with_pics):
            img_name = f'{image_name}{image_enum}.jpg'
            logger.info(f'START download {link} to {cur_dir}')
            url_tuple = urlparse(link)
            headers['Host'] = url_tuple[1]
            resp = requests.get(link, headers=headers)
            logger.info(f'Результат ссылки {link} на существование:{resp.status_code}')
            if not resp.ok:
                return exit(1)
            with open(os.path.join(image_path, img_name), 'wb') as q:
                q.write(resp.content)
            logger.info(f'Скачали файл {img_name} по ссылке:{link}')
    except Exception as e:
        logger.error(f'{e}')
        print(f'{e}')
    return


if __name__ == '__main__':
    fetch_spacex()
