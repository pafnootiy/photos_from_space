import os
import time
import telegram
from os import listdir
from os.path import isfile
from os.path import join as joinpath
from dotenv import load_dotenv


def send_photo_in_tg(filepath):
    with open(filepath, 'rb') as file:
        image_file = file.read()
    return image_file


def main():

    load_dotenv()

    bot = telegram.Bot(token=os.getenv("TG_TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    bot_time = os.getenv("TIME")
    while True:

        apod_path = "apod_pics"
        for photo in listdir(apod_path):
            if isfile(joinpath(apod_path, photo)):
                filepath = f'apod_pics/{photo}'
                bot.send_document(chat_id=chat_id, document=send_photo_in_tg(filepath))
        image_path = "images"

        for photo in listdir(image_path):
            if isfile(joinpath(image_path, photo)):
                filepath = f'images/{photo}'
                bot.send_document(chat_id=chat_id, document=send_photo_in_tg(filepath))

        epic_path = "epic_pics"
        for photo in listdir(epic_path):
            if isfile(joinpath(epic_path, photo)):
                filepath = f'epic_pics/{photo}'
                bot.send_document(chat_id=chat_id, document=send_photo_in_tg(filepath))
        time.sleep(int(bot_time))


if __name__ == "__main__":
    main()