from pathlib import Path

import requests
import urllib3
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
        print(book_path)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    else:
        pass


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    for book_id in range(1, 2):
        url = f"https://tululu.org/txt.php?id={book_id}"
        try:
            download_txt(url, "Али\\би", folder="txt/")
        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue


if __name__ == "__main__":
    main()
