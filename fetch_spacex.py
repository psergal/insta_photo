import requests
import os
import pathlib
import random
from urllib.parse import urlparse
import args_handle


def fetch_spacex():
    image_folder = args_handle.get_args()
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, image_folder)
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
    resp = requests.get(spacex_api, headers=headers)
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
        img_name = f'{image_name}{image_enum}.{pathlib.Path(link).suffix}'
        url_tuple = urlparse(link)
        headers['Host'] = url_tuple[1]
        resp = requests.get(link, headers=headers)
        if not resp.ok:
            return exit(1)
        with open(os.path.join(image_path, img_name), 'wb') as q:
            q.write(resp.content)
        print(f'file {img_name}: Done!')


if __name__ == '__main__':
    fetch_spacex()
