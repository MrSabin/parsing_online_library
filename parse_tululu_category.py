from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup


def parse_page(response):
    soup = BeautifulSoup(response.text, "lxml")
    book_id = soup.select_one("#content .d_book a")
    book_url = urljoin(response.url, book_id["href"])
    print(book_url)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://tululu.org/l55/"
    response = requests.get(url, verify=False)
    response.raise_for_status()

    parse_page(response)


if __name__ == "__main__":
    main()
