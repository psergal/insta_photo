#settings.py
import os
from dotenv import load_dotenv

load_dotenv()
headers = {
    'User-Agent': 'curl',
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8',
    'Connection': 'Keep-Alive'
}
cur_dir = os.path.dirname(__file__)
image_path = os.path.join(cur_dir, 'images')
image_name = 'space'
spacex_api = 'https://api.spacexdata.com/v3/launches'
hubble_api = "http://hubblesite.org/api/v3/image/"
hubble_img_id = '3811'
mode = 'latest'
