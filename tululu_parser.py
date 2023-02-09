from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = "https://tululu.org/b9/"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")
book_with_author = soup.find("h1").text.split("::")
book = book_with_author[0].strip()
author = book_with_author[1].strip()
image_partial_url = soup.find("div", class_="bookimage").find("img")["src"]

base_url = "https://tululu.org"
img_url = urljoin(base_url, image_partial_url)
