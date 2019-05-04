import requests
import random
import args_handle
from load_store import load_n_store

def fetch_spacex():
    args = args_handle.get_args()
    resp = requests.get(args.api, headers=args.headers)
    if not resp.ok:
        return exit(1)
    flights_with_links = {flight.get('flight_number'): flight['links'].get('flickr_images')
                          for flight in resp.json() if len(flight['links'].get('flickr_images')) > 0}
    flight_with_pics = {}
    if args.flight_mode == 'random':
        flight_with_pics = random.choice(flights_with_links)
    elif args.flight_mode == 'latest':
        flight_with_pics = flights_with_links.get(max(flights_with_links.keys()))
    written_files = load_n_store(flight_with_pics, args.img_name, args.img_dir)
    return written_files


if __name__ == '__main__':
    fetch_spacex()
