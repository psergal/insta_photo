import requests
import args_handle
from load_store import load_n_store

def fetch_hubble():
    '''
    function calls args_handle(), gets service, place to store and image's id
    puts list of links to the call of load_n_store()
    :return: list of stored images
    '''
    args = args_handle.get_args()
    resp = requests.get(f'{args.api}/{args.img_id}', headers=args.headers)
    if not resp.ok:
        return exit(1)
    img_links = [image_file.get('file_url') for image_file in resp.json().get('image_files')]
    written_files = load_n_store(img_links, args.img_name, args.img_dir)
    return written_files

if __name__ == '__main__':
    fetch_hubble()
