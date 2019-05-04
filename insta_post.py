import os
from dotenv import load_dotenv
from instabot import Bot
import args_handle


def insta_upload():
    args = args_handle.get_args()
    load_dotenv()
    inst_name = os.getenv('inst_name')
    inst_pass = os.getenv('inst_pass')
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, args.img_dir)
    pics = os.listdir(image_path)
    if len(pics) == 0:
        return exit(1)
    bot = Bot()
    bot.login(username=inst_name, password=inst_pass, proxy=None)

    for enum, pic in enumerate(pics):
        caption = f'picture {enum} file name {pic}'
        pic_full_path = os.path.join(image_path, pic)
        bot.upload_photo(pic_full_path, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            break


if __name__ == '__main__':
    insta_upload()