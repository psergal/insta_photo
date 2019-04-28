import requests
import logging
import http.client as httplib
import os
import sys
import pathlib
from urllib.parse import urlparse


def link_to_pic_name(url):
    return url.split('/')[-1], url.split('.')[-1]


def download(url, headers, filename, logger):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True, headers=headers)
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


def fetch_hubble():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    httplib.HTTPConnection.debuglevel = 0  # 1 -включает
    logging.basicConfig(filename='insta.log', level=logging.DEBUG, format=log_format, filemode='w')
    logger = logging.getLogger("requests.packages.urllib3")
    logger.info(f'START {fetch_hubble.__name__}')

    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, 'images')
    image_id = '3851'
    hubble_api = "http://hubblesite.org/api/v3/image/"
    url_tuple = urlparse(hubble_api)
    headers = {
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    }
    headers['Host'] = url_tuple[1]
    pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)
    logger.info(f'START download {image_id} to {cur_dir}')
    try:
        resp = requests.get(f'{hubble_api}/{image_id}', headers=headers)
        logger.info(f'Результат ссылки {hubble_api}/{image_id} на существование:{resp.status_code}')
        if not resp.ok:
            return exit(1)
        img_links = [image_file.get('file_url') for image_file in resp.json().get('image_files')]
        for image_enum, link in enumerate(img_links):
            link_f_name, link_f_ext = link_to_pic_name(link)
            img_name = f'{image_id}{image_enum}.{link_f_ext}'
            url_tuple = urlparse(link)
            headers['Host'] = url_tuple[1]
            logger.info(f'START download {link} to {cur_dir}')
            print(f'[*] Downloading test file{img_name}')
            download(link, headers, os.path.join(image_path, img_name), logger)
            print('[*] Done!')
    except Exception as e:
        logger.error(f'{e}')
        print(f'{e}')
    return


if __name__ == '__main__':
    fetch_hubble()
