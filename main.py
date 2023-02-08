from pathlib import Path

import requests
import urllib3


def download_book(path, book_id):
    url = f"https://tululu.org/txt.php?id={book_id}"
    name = f"{book_id}.txt"

    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    filename = Path(path, name)
    with open(filename, "w") as file:
        file.write(response.text)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    path = "books"
    Path(path).mkdir(parents=True, exist_ok=True)

    for book_id in range(1, 11):
        try:
            download_book(path, book_id)
        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue


if __name__ == "__main__":
    main()
