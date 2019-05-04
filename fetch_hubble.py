import requests
import os
import pathlib
from urllib.parse import urlparse
import args_handle


def fetch_hubble():
    image_folder = args_handle.get_args()
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, image_folder)
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
    resp = requests.get(f'{hubble_api}/{image_id}', headers=headers)
    if not resp.ok:
        return exit(1)
    img_links = [image_file.get('file_url') for image_file in resp.json().get('image_files')]
    for image_enum, link in enumerate(img_links):
        img_name = f'{image_id}_{image_enum}{pathlib.Path(link).suffix}'
        url_tuple = urlparse(link)
        headers['Host'] = url_tuple[1]
        resp = requests.get(link, headers=headers)
        if not resp.ok:
            return exit(1)
        with open(os.path.join(image_path, img_name), 'wb') as q:
            q.write(resp.content)
        print(f'file {img_name}: Done!')


if __name__ == '__main__':
    fetch_hubble()
