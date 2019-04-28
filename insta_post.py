import logging
import http.client as httplib
import os
from dotenv import load_dotenv
from instabot import Bot


def isnta_upload():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    httplib.HTTPConnection.debuglevel = 0  # 1 -включает
    logging.basicConfig(filename='insta.log', level=logging.DEBUG, format=log_format, filemode='w')
    logger = logging.getLogger("requests.packages.urllib3")
    logger.info(f'START {isnta_upload.__name__}')
    load_dotenv()
    inst_name = os.getenv('inst_name')
    inst_pass = os.getenv('inst_pass')
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, 'images')

    logger.info(f'Start uploading to the Instagram account {inst_name}')
    pics = os.listdir(image_path)

    bot = Bot()
    bot.login(username=inst_name, password=inst_pass, proxy=None)

    for enum, pic in enumerate(pics):
        caption = f'picture {enum} file name {pic}'
        pic_full_path = os.path.join(image_path, pic)
        bot.upload_photo(pic_full_path, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            logger.error(bot.api.last_response)
            break
    return


if __name__ == '__main__':
    isnta_upload()