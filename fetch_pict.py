import requests
from urllib.parse import urlparse
import logging
import http.client as httplib
import os
import pathlib
import json
import random
import settings


def link_to_pic_name(url):
    return url.split('/')[-1], url.split('.')[-1]


def fetch_hubble_imgs (hubble_api, image_id, logger):
    logger.info(f'START {fetch_hubble_imgs.__name__}')
    url_tuple = urlparse(hubble_api)
    settings.headers['Host'] = url_tuple[1]
    logger.info(f'START download {image_id} to {settings.cur_dir}')
    settings.headers['Host'] = url_tuple[1]
    resp = requests.get(f'{hubble_api}/{image_id}', headers=settings.headers)
    logger.info(f'Результат ссылки {hubble_api} на существование:{resp.status_code}')
    if not resp.ok:
        return exit(1)
    img_links =[image_file.get('file_url')  for image_file in resp.json().get('image_files')]
    pathlib.Path(settings.image_path).mkdir(parents=True, exist_ok=True)
    for image_enum, link in enumerate(img_links):
        link_f_name, link_f_ext = link_to_pic_name(link)
        img_name = f'{image_id}{image_enum}.{link_f_ext}'
        url_tuple = urlparse(link)
        settings.headers['Host'] = url_tuple[1]
        logger.info(f'START download {link} to {settings.cur_dir}')
        resp = requests.get(link, headers=settings.headers)
        logger.info(f'Результат ссылки {link} на существование:{resp.status_code}')
        if not resp.ok:
            return exit(1)
        with open(os.path.join(settings.image_path, img_name), 'wb') as q:
            q.write(resp.content)
        logger.info(f'Скачали файл {img_name} по ссылке:{link}')
    return


def insta():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    httplib.HTTPConnection.debuglevel = 0  # 1 -включает
    logging.basicConfig(filename='insta.log', level=logging.DEBUG, format=log_format, filemode='w')
    logger = logging.getLogger("requests.packages.urllib3")
    logger.info(f'START {insta.__name__}')
    # fetch_spacex_last_launch(settings.spacex_api, settings.mode, logger)
    fetch_hubble_imgs(settings.hubble_api, settings.hubble_img_id, logger)

def fetch_spacex_last_launch(spacex_api, flight_mode, logger):
    logger.info(f'START {fetch_spacex_last_launch.__name__}')
    url_tuple = urlparse(spacex_api)
    settings.headers['Host'] = url_tuple[1]
    resp = requests.get(spacex_api, headers=settings.headers)
    logger.info(f'Результат ссылки {spacex_api} на существование:{resp.status_code}')
    if not resp.ok:
        return exit(1)
    flights_with_links = {flight.get('flight_number'): flight['links'].get('flickr_images') for flight in resp.json()
                          if len(flight['links'].get('flickr_images')) > 0}
    flight_with_pics = {}
    if flight_mode == 'random':
        flight_with_pics = random.choice(flights_with_links)
    elif flight_mode == 'latest':
        flight_with_pics = flights_with_links.get(max(flights_with_links.keys()))
    pathlib.Path(settings.image_path).mkdir(parents=True, exist_ok=True)
    for image_enum, link in enumerate(flight_with_pics):
        img_name = f'{settings.image_name}{image_enum}.jpg'
        url_tuple = urlparse(link)
        settings.headers['Host'] = url_tuple[1]
        logger.info(f'START download {link} to {settings.cur_dir}')
        resp = requests.get(link, headers=settings.headers)
        logger.info(f'Результат ссылки {link} на существование:{resp.status_code}')
        if not resp.ok:
            return exit(1)
        with open(os.path.join(settings.image_path, img_name), 'wb') as q:
            q.write(resp.content)
        logger.info(f'Скачали файл {img_name} по ссылке:{link}')
    return


if __name__ == '__main__':
    insta()
