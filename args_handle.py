import argparse
import inspect

def get_args():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    desc = ''
    if calframe[1][3] == 'fetch_hubble':
        desc = "Downloading pictures about space from Hubble"
    elif calframe[1][3] == 'fetch_space':
        desc = "Downloading pictures about space from SpaceX"
    elif calframe[1][3] == 'insta_posrt':
        desc = "Posting images from local folder"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dir', default='images',  help='Define image folder default=images')
    args = parser.parse_args()

    return args.dir

if __name__ == '__main__':
    get_args()
