from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup


def parse_page(response):
    soup = BeautifulSoup(response.text, "lxml")
    book_ids = [
        content.a["href"] for content in soup.select("#content .d_book")
    ]
    book_urls = [urljoin(response.url, book_id) for book_id in book_ids]
    print(book_urls)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://tululu.org/l55/"
    response = requests.get(url, verify=False)
    response.raise_for_status()

    parse_page(response)


if __name__ == "__main__":
    main()
