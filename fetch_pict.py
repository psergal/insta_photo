import requests
from urllib.parse import urlparse
import logging
import http.client as httplib
import os
import pathlib
import sys
import random
import settings
from instabot import Bot


def download(url, filename, logger):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True, headers=settings.headers)
        total = response.headers.get('content-length')

        if total is None:
            logger.error(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')


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

    for image_enum, link in enumerate(img_links):
        link_f_name, link_f_ext = link_to_pic_name(link)
        img_name = f'{image_id}{image_enum}.{link_f_ext}'
        url_tuple = urlparse(link)
        settings.headers['Host'] = url_tuple[1]
        logger.info(f'START download {link} to {settings.cur_dir}')
        print(f'[*] Downloading test file{img_name}')
        download(link, os.path.join(settings.image_path, img_name),logger)
        print('[*] Done!')
    return


def insta():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    httplib.HTTPConnection.debuglevel = 0  # 1 -включает
    logging.basicConfig(filename='insta.log', level=logging.DEBUG, format=log_format, filemode='w')
    logger = logging.getLogger("requests.packages.urllib3")
    logger.info(f'START {insta.__name__}')
    try:
        pathlib.Path(settings.image_path).mkdir(parents=True, exist_ok=True)
        fetch_spacex_last_launch(settings.spacex_api, settings.mode, logger)
        fetch_hubble_imgs(settings.hubble_api, settings.hubble_img_id, logger)
        isnta_upload(logger)
    except Exception as e:
        logger.error(e)
        print(str(e))
    return


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


def isnta_upload(logger):
    logger.info(f'Start uploading to the Instagram account {settings.inst_name}')
    pics = os.listdir(settings.image_path)

    bot = Bot()
    bot.login(username=settings.inst_name, password=settings.inst_pass, proxy=None)

    for enum, pic in enumerate(pics):
        caption = f'picture {enum} file name {pic}'
        pic_full_path = os.path.join(settings.image_path, pic)
        bot.upload_photo(pic_full_path, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            logger.error(bot.api.last_response)
            break

    return


if __name__ == '__main__':
    insta()
