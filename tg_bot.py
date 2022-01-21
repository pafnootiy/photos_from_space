import os
import time
import telegram
from os import listdir
from os.path import isfile
from os.path import join as joinpath
from dotenv import load_dotenv


def post_photo_in_tg(folder, chat_id, bot):
    for photo in listdir(folder):
        if isfile(joinpath(folder, photo)):
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
    while True:
        for folder in folders:
            time.sleep(int(bot_time))
            post_photo_in_tg(folder, chat_id, bot)


if __name__ == "__main__":
    main()