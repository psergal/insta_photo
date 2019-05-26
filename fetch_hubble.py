import requests
import argparse
import load_store as ls


def fetch_hubble():
    """
    function calls args_handle(), gets service, place to store and image's id
    puts list of links to the call of load_n_store()
    :return: list of stored images
    """
    args = get_args()
    resp = requests.get(f'{args.api}/{args.img_id}', headers=args.headers)
    if not resp.ok:
        return None
    img_links = [image_file.get('file_url') for image_file in resp.json().get('image_files')]
    written_files = ls.load_n_store(img_links, args.img_name, args.img_dir)
    for link_number, written_file in enumerate(written_files):
        print(f'From {args.api} link_number-{link_number} has been downloaded and stored to {args.img_dir} folder as \
        {written_file}')


def get_args():
    parser = argparse.ArgumentParser(description='Downloading pictures about space from Hubble')
    parser.add_argument('--img_name', default='hubble',  help='Define image name default=hubble')
    parser.add_argument('--img_id', default='3851',  help='Define image id default=3851')
    parser.add_argument('--api', default='http://hubblesite.org/api/v3/image/', help=argparse.SUPPRESS)
    parser.add_argument('--headers', default={
        'Host': 'hubblesite.org',
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    }, help=argparse.SUPPRESS)
    parser.add_argument('--img_dir', default='images',  help='Define image folder default=images')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    fetch_hubble()
