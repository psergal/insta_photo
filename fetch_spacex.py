import requests
import random
import argparse
import load_store as ls


def fetch_spacex():
    args = get_args()
    resp = requests.get(args.api, headers=args.headers)
    if not resp.ok:
        return None
    flights_with_links = {flight.get('flight_number'): flight['links'].get('flickr_images')
                          for flight in resp.json() if len(flight['links'].get('flickr_images')) > 0}
    flight_with_pics = {}
    if args.flight_mode == 'random':
        flight_with_pics = random.choice(flights_with_links)
    elif args.flight_mode == 'latest':
        flight_with_pics = flights_with_links.get(max(flights_with_links.keys()))
    written_files = ls.load_n_store(flight_with_pics, args.img_name, args.img_dir)
    for link_number, written_file in enumerate(written_files):
        print(f'From {args.api} link_number-{link_number} has been downloaded and stored to {args.img_dir} folder as\
        {written_file}')


def get_args():
    parser = argparse.ArgumentParser(description='Downloading pictures about space from SpaceX')
    parser.add_argument('--img_name', default='spacex',  help='Define image name default=space')
    parser.add_argument('--flight_mode', default='latest', choices=['latest', 'random'],
                        help='Which flight latest or random')
    parser.add_argument('--api', default='https://api.spacexdata.com/v3/launches', help=argparse.SUPPRESS)
    parser.add_argument('--headers', default={
        'Host': 'api.spacexdata.com',
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    },  help=argparse.SUPPRESS)
    parser.add_argument('--img_dir', default='images',  help='Define image folder default=images')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    fetch_spacex()
