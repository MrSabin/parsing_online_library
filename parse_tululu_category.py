import json
import time
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import requests
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

from main import (
    check_for_redirect,
    download_image,
    download_txt,
    parse_book_page,
)


def parse_category_page(response):
    soup = BeautifulSoup(response.text, "lxml")
    book_ids = [
        content.a["href"] for content in soup.select("#content .d_book")
    ]
    book_urls = [urljoin(response.url, book_id) for book_id in book_ids]
    return book_urls


def write_json(books_dump, folder="json/"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = Path(folder, "books_dump.json")
    with open(filepath, "w") as file:
        json.dump(books_dump, file, ensure_ascii=False, indent=4)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    all_book_urls = []
    print("Fetching book urls...")
    for page_number in tqdm(range(1, 5)):

        url = f"https://tululu.org/l55/{page_number}"
        response = requests.get(url, verify=False)
        response.raise_for_status()

        page_book_urls = parse_category_page(response)
        all_book_urls.extend(page_book_urls)

    print("Downloading books...")
    books_dump = []

    for book_url in tqdm(all_book_urls):
        try:
            response = requests.get(book_url, verify=False)
            response.raise_for_status()
            check_for_redirect(response)

            parsed_page = parse_book_page(response)
            splitted_url = urlsplit(unquote(response.url))
            book_id = splitted_url.path.replace("/", "")[1:]
            book_path = download_txt(book_id, parsed_page["book_name"])
            parsed_page["book_path"] = str(book_path)
            image_path = download_image(parsed_page["image_url"])
            parsed_page["img_src"] = str(image_path)
            parsed_page.pop("image_url", None)
            books_dump.append(parsed_page)
        except requests.HTTPError:
            continue
        except requests.ConnectionError:
            print("Connection error, retrying in 10 seconds...")
            time.sleep(10)
    write_json(books_dump)


if __name__ == "__main__":
    main()
