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
    return book_urls


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    all_book_urls = []
    for page_number in range(1, 11):
        url = f"https://tululu.org/l55/{page_number}"
        response = requests.get(url, verify=False)
        response.raise_for_status()

        page_book_urls = parse_page(response)
        all_book_urls.extend(page_book_urls)
    print(all_book_urls)


if __name__ == "__main__":
    main()
