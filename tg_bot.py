import os
import time
import telegram
from os import listdir
from os.path import isfile
from os.path import join as joinpath
from dotenv import load_dotenv


def main():

    load_dotenv()

    bot = telegram.Bot(token=os.getenv("TG_TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    bot_time = os.getenv("TIME")
    while True:
        path = "apod_pics"
        for photo in listdir(path):
            if isfile(joinpath(path, photo)):
                filepath = f'apod_pics/{photo}'
                with open(filepath, 'rb') as file:
                    image_file = file.read()
                bot.send_document(chat_id=chat_id, document=image_file)
        time.sleep(int(bot_time))


if __name__ == "__main__":
    main()