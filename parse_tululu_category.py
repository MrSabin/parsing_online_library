import argparse
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


def fetch_last_page():
    url = "https://tululu.org/l55/"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    last_page = soup.select("#content .center .npage")[-1].text

    return int(last_page)


def initialize_argparse():
    parser = argparse.ArgumentParser(
        description="Script for download books by category"
    )
    parser.add_argument(
        "--start_page", type=int, help="Starting from this page"
    )
    parser.add_argument("--end_page", type=int, help="Ends with this page")
    parser.add_argument(
        "--dest_folder", help="Destination folder", default=Path.cwd()
    )
    parser.add_argument(
        "--skip_images", action="store_true", help="Skip images download"
    )
    parser.add_argument(
        "--skip_txt", action="store_true", help="Skip text download"
    )
    parser.add_argument("--json_path", type=str, help="Folder for JSON dump")

    return parser


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = initialize_argparse()
    args = parser.parse_args()
    if not args.end_page:
        args.end_page = fetch_last_page()

    all_book_urls = []
    books_dump = []

    print("Fetching book urls...")
    for page_number in tqdm(range(args.start_page, args.end_page)):
        try:
            url = f"https://tululu.org/l55/{page_number}"
            response = requests.get(url, verify=False)
            response.raise_for_status()
            check_for_redirect(response)
            page_book_urls = parse_category_page(response)
            all_book_urls.extend(page_book_urls)

        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue
        except requests.ConnectionError:
            print("Connection error, retrying in 10 seconds...")
            time.sleep(10)

    print("Downloading books...")
    for book_url in tqdm(all_book_urls):
        try:
            response = requests.get(book_url, verify=False)
            response.raise_for_status()
            check_for_redirect(response)

            parsed_page = parse_book_page(response)
            splitted_url = urlsplit(unquote(response.url))
            book_id = splitted_url.path.replace("/", "")[1:]
            if not args.skip_txt:
                book_path = download_txt(book_id, parsed_page["book_name"])
                parsed_page["book_path"] = str(book_path)
            if not args.skip_images:
                image_path = download_image(parsed_page["image_url"])
                parsed_page["img_src"] = str(image_path)
            parsed_page.pop("image_url", None)
            books_dump.append(parsed_page)
        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue
        except requests.ConnectionError:
            print("Connection error, retrying in 10 seconds...")
            time.sleep(10)
    write_json(books_dump, args.json_path)


if __name__ == "__main__":
    main()
