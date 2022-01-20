import os
import time
import telegram
from os import listdir
from os.path import isfile
from os.path import join as joinpath
from dotenv import load_dotenv


def post_photo_in_tg(folder, chat_id, bot):
    path_to_folder = folder
    for photo in listdir(path_to_folder):
        if isfile(joinpath(path_to_folder, photo)):
            filepath = f'{folder}/{photo}'
            with open(filepath, 'rb') as file:
                image_file = file.read()
                bot.send_document(chat_id=chat_id, document=image_file)


def main():
    load_dotenv()
    folders = ["apod_pics", "images", "epic_pics"]
    bot = telegram.Bot(token=os.getenv("TG_TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    bot_time = os.getenv("TIME")
    for folder in folders:
        print(folder)
        post_photo_in_tg(folder, chat_id, bot)
    while True:
        time.sleep(int(bot_time))


if __name__ == "__main__":
    main()