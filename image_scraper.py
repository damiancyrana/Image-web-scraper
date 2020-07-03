from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os


def start_search():
    search = input("Search for: ")
    params = {"q": search}
    name = search.replace(" ", "_").lower()

    if not os.path.isdir(name):
        os.makedirs(name)

    r = requests.get("http://www.bing.com/images/search", params=params)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.findAll("a", {"class": "thumb"})

    for picture in links:
        try:
            image_obj = requests.get(picture.attrs["href"])
            print("Getting -->", picture.attrs["href"])
            title = picture.attrs["href"].split("/")[-1]
            try:
                image = Image.open(BytesIO(image_obj.content))
                image.save("./" + name + "/" + title, image.format)
            except:
                print("Couldn't save image")
        except:
            print("Couldn't request image")

    start_search()


start_search()
