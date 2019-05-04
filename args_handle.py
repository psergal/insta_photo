import argparse
import inspect

def get_args():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    if calframe[1][3] == 'fetch_hubble':
        parser = argparse.ArgumentParser(description='Downloading pictures about space from Hubble')
        parser.add_argument('--img_name', default='hubble',  help='Define image name default=hubble')
        parser.add_argument('--img_id', default='3851',  help='Define image id default=3851')
        parser.add_argument('--api', default='http://hubblesite.org/api/v3/image/',
                            help=argparse.SUPPRESS)
        parser.add_argument('--headers', default={
            'Host': 'hubblesite.org',
            'User-Agent': 'curl',
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'Keep-Alive'
        }, help=argparse.SUPPRESS)
    elif calframe[1][3] == 'fetch_spacex':
        parser = argparse.ArgumentParser(description='Downloading pictures about space from SpaceX')
        parser.add_argument('--img_name', default='spacex',  help='Define image name default=space')
        parser.add_argument('--flight_mode', default='latest', choices=['latest', 'random'],
                            help='Which flight latest or random')
        parser.add_argument('--api', default='https://api.spacexdata.com/v3/launches',
                            help=argparse.SUPPRESS)
        parser.add_argument('--headers', default={
            'Host': 'api.spacexdata.com',
            'User-Agent': 'curl',
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'Keep-Alive'
            },  help=argparse.SUPPRESS)
    elif calframe[1][3] == 'insta_upload':
        parser = argparse.ArgumentParser(description='Posting images from local folder')

    parser.add_argument('--img_dir', default='images',  help='Define image folder default=images')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    get_args()
