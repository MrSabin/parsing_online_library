from pathlib import Path

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(url, filename, folder="books/"):
    sanitized_filename = sanitize_filename(filename)
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    book_path = Path(folder, f"{sanitized_filename}.txt")
    with open(book_path, "w") as file:
        file.write(response.text)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


def parse_book_name(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, "lxml")
    book_with_author = soup.find("h1").text.split("::")
    book = book_with_author[0].strip()
    author = book_with_author[1].strip()

    return book


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    for book_id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={book_id}"
        try:
            filename = parse_book_name(book_id)
            download_txt(url, filename)
        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue


if __name__ == "__main__":
    main()
