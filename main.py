from pathlib import Path
from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(book_id, filename, folder="books/"):
    url = f"https://tululu.org/txt.php?id={book_id}"
    sanitized_filename = sanitize_filename(filename)
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    book_path = Path(folder, f"{book_id}. {sanitized_filename}.txt")
    with open(book_path, "w") as file:
        file.write(response.text)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


def parse_book_page(book_id):
    base_url = "https://tululu.org"
    page_url = urljoin(base_url, f"b{book_id}/")
    response = requests.get(page_url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, "lxml")
    book_with_author = soup.find("h1").text.split("::")
    book = book_with_author[0].strip()
    image_partial_url = soup.find("div", class_="bookimage").find("img")["src"]
    image_url = urljoin(base_url, image_partial_url)

    return book


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for book_id in range(1, 11):
        try:
            filename = parse_book_page(book_id)
            download_txt(book_id, filename)
        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue


if __name__ == "__main__":
    main()
