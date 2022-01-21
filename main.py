import datetime
import os
from pathlib import Path
import requests
from dotenv import load_dotenv


def get_flight_urls(flight_number):
    url = 'https://api.spacexdata.com/v3/launches/'
    payload = {
        'flight_number': flight_number
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    return response[0]['links']['flickr_images']


def fetch_spacex_last_launch(flight_number, path_for_images_photos):
    Path(path_for_images_photos).mkdir(parents=True, exist_ok=True)
    for number, link in enumerate(get_flight_urls(flight_number)):
        filename = Path("images", f'spacex{number}.jpeg')
        response = requests.get(link)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def get_apod_urls(api_key):
    apod_url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "api_key": api_key,
        "count": 15
    }
    response = requests.get(apod_url, params=payload)
    response = response.json()
    apod_photo_links = []
    for photo_links in response:
        apod_photo_links.append(photo_links['url'])
    return apod_photo_links


def download_apod_photos(api_key, path_for_apod_photos):
    Path(path_for_apod_photos).mkdir(parents=True, exist_ok=True)
    for numbers, link in enumerate(get_apod_urls(api_key)):
        filename = Path("apod_pics", f'apod_pics{numbers}.jpeg')
        response = requests.get(link)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def get_epic_links(api_key):
    epic_link = "https://api.nasa.gov/EPIC/api/natural/date/2021-12-13"
    payload = {
        "api_key": api_key
    }
    response = requests.get(epic_link, params=payload)
    response = response.json()
    date_link = response[0]["date"]
    image_name = response[0]["image"]
    date = datetime.datetime.fromisoformat(date_link)
    epic_photo_links = []
    for image in response:
        epic_photo_link = f"https://api.nasa.gov/EPIC/archive/natural/" \
                          f"{date.year}/{date.month}/{date.day}/png/" \
                          f"{image['image']}.png"
        epic_photo_links.append(epic_photo_link)
    return epic_photo_links


def download_epic_photos(api_key, path_for_epic_photos):
    Path(path_for_epic_photos).mkdir(parents=True, exist_ok=True)
    for number, links in enumerate(get_epic_links(api_key)):
        filename = Path("epic_pics", f'epic_pics{number}.jpeg')
        payload = {
            "api_key": api_key
        }
        response = requests.get(links, params=payload)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def main():
    load_dotenv()
    api_key = os.getenv("NASA_TOKEN")
    flight_number = 107
    path_for_images_photos = "photos_from_space/images"
    path_for_apod_photos = "photos_from_space/apod_pics"
    path_for_epic_photos = 'photos_from_space/epic_pics'
    fetch_spacex_last_launch(flight_number, path_for_images_photos)
    download_apod_photos(api_key, path_for_apod_photos)
    download_epic_photos(api_key, path_for_epic_photos)


if __name__ == "__main__":
    main()
