import requests
from pathlib import Path
import os
import datetime
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
    Path('C:/Users/Alex K/p_p/space_photos/images').mkdir(parents=True, exist_ok=True)
    for numbers, link in enumerate(get_image_url(url)):
        filename = Path("images", f'spacex{numbers}.jpeg')
        response = requests.get(link)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def get_url_extension(nasa_url):
    response = requests.get(nasa_url)
    extension = os.path.splitext(response.json()['hdurl'])
    return extension[1]


def get_apod(apod_url):
    api_key = os.getenv("API_KEY")
    payload = {
        "api_key": api_key,
        "count": 15
    }
    response = requests.get(apod_url, params=payload)
    response = response.json()
    apod_photo_links = []
    for num, photo_links in enumerate(response):
        apod_photo_links.append(photo_links['url'])
    return apod_photo_links


def get_apod_photo(apod_url):
    Path('C:/Users/Alex K/p_p/space_photos/apod_pics').mkdir(parents=True, exist_ok=True)
    for numbers, link in enumerate(get_apod(apod_url)):
        filename = Path("apod_pics", f'apod_pics{numbers}.jpeg')
        response = requests.get(link)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def get_epic_link(epic_link):
    api_key = os.getenv("API_KEY")
    payload = {
        "api_key": api_key,
        "enhanced/date": "2021-06-23"
    }
    response = requests.get(epic_link, params=payload)
    response = response.json()
    date_for_link = response[0]["date"]
    date = datetime.datetime.fromisoformat(date_for_link)
    epic_photo_link_list = []

    for image in response:
        epic_photo_link = f"https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date.month}/" \
                          f"{date.day}/png/{image['image']}.png?api_key=DEMO_KEY"
        epic_photo_link_list.append(epic_photo_link)
    return epic_photo_link_list


def get_epic_photo(epic_link):
    Path('C:/Users/Alex K/p_p/space_photos/epic_pics').mkdir(parents=True, exist_ok=True)
    for number, links in enumerate(get_epic_link(epic_link)):
        filename = Path("epic_pics", f'epic_pics{number}.jpeg')
        response = requests.get(links)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def main():
    load_dotenv()
    url = 'https://api.spacexdata.com/v3/launches/'
    nasa_url = "https://api.nasa.gov/planetary/apod?api_key=pi89FIExpKRQvAQgJYMTfzLCoIVyGHjQtVT1WR4K"
    apod_url = "https://api.nasa.gov/planetary/apod"
    epic_link = "https://api.nasa.gov/EPIC/api/natural/images?api_key=DEMO_KEY"
    get_image_url(url)
    fetch_spacex_last_launch(url)
    get_url_extension(nasa_url)
    get_apod(apod_url)
    get_apod_photo(apod_url)
    get_epic_link(epic_link)
    get_epic_photo(epic_link)


if __name__ == "__main__":
    main()
