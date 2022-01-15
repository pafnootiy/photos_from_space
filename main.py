import datetime
import os
from pathlib import Path
import requests
from dotenv import load_dotenv


def get_image_url(url):
    payload = {
        'flight_number': "107"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    return response[0]['links']['flickr_images']


def fetch_spacex_last_launch(url):
    Path('photos_from_space/images').mkdir(parents=True, exist_ok=True)
    for numbers, link in enumerate(get_image_url(url)):
        filename = Path("images", f'spacex{numbers}.jpeg')
        response = requests.get(link)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)




def get_url_extension(apod_url):
    api_key = os.getenv("API_KEY")
    payload = {
        "api_key": api_key,
    }
    response = requests.get(apod_url, params=payload)
    extension = os.path.splitext(response.json()['hdurl'])
    return print(extension[1])


def get_apod(apod_url):
    api_key = os.getenv("API_KEY")
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


def get_apod_photo(apod_url):
    Path('photos_from_space/apod_pics').mkdir(parents=True, exist_ok=True)
    for numbers, link in enumerate(get_apod(apod_url)):
        filename = Path("apod_pics", f'apod_pics{numbers}.jpeg')
        response = requests.get(link)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def get_epic_link(epic_link):
    api_key = os.getenv("API_KEY")
    payload = {
        "api_key": api_key
    }
    response = requests.get(epic_link, params=payload)
    response = response.json()
    date_link = response[0]["date"]
    image_name = response[0]["image"]
    date = datetime.datetime.fromisoformat(date_link)
    epic_photo_link = f"https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date.month}/{date.day}/png/{image_name}.png"
    epic_photo_link_list = []

    for image in response:
        epic_photo_link = f"https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date.month}/" \
                              f"{date.day}/png/{image['image']}.png"
        epic_photo_link_list.append(epic_photo_link)
    return epic_photo_link_list


def get_epic_photo(epic_link):
    api_key = os.getenv("API_KEY")
    Path('photos_from_space/epic_pics').mkdir(parents=True, exist_ok=True)
    for number, links in enumerate(get_epic_link(epic_link)):
        filename = Path("epic_pics", f'epic_pics{number}.jpeg')
        payload = {
            "api_key": api_key
        }
        response = requests.get(links,params=payload)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def main():
    load_dotenv()
    url = 'https://api.spacexdata.com/v3/launches/'
    apod_url = "https://api.nasa.gov/planetary/apod"
    epic_link = "https://api.nasa.gov/EPIC/api/natural/date/2021-12-13"
    get_image_url(url)
    fetch_spacex_last_launch(url)
    get_url_extension(apod_url)
    get_apod(apod_url)
    get_apod_photo(apod_url)
    get_epic_link(epic_link)
    get_epic_photo(epic_link)

if __name__ == "__main__":
    main()