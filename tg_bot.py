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
    updates = bot.get_updates()
    chat_id = os.getenv("CHAT_ID")
    while True:
        path = "apod_pics"
        for photo in listdir(path):
            if isfile(joinpath(path, photo)):
                bot.send_document(chat_id=chat_id, document=open(f'apod_pics/{photo}', 'rb'))
        time.sleep(30)
if __name__ == "__main__":
    main()