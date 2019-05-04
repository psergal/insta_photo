import requests
import os
import pathlib


def load_n_store(links, image_name, folder):
    '''
    Load files that came in the list of :links
    with name's boilerplate :image_name
    into the folder that was passed in the :folder parameter
    '''
    if len(links)<1:
        return None
    list_of_files = []
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, folder)
    pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)
    for image_enum, link in enumerate(links):
        img_name = f'{image_name}{image_enum}{pathlib.Path(link).suffix}'
        resp = requests.get(link)
        if not resp.ok:
            return exit(1)
        with open(os.path.join(image_path, img_name), 'wb') as q:
            q.write(resp.content)
        print(f'file {img_name}: Done!')
        list_of_files.append(img_name)
    return list_of_files


if __name__ == '__main__':
    load_n_store()
