import argparse
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(book_id, filename, folder="books/"):
    url = "https://tululu.org/txt.php"
    payload = {"id": book_id}
    sanitized_filename = sanitize_filename(filename)
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    book_path = Path(folder, f"{book_id}. {sanitized_filename}.txt")
    with open(book_path, "w") as file:
        file.write(response.text)


def download_image(image_url, folder="images/"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    splitted_url = urlsplit(unquote(image_url), allow_fragments=True)
    splitted_path = splitted_url.path.split("/")[-1]
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    image_path = Path(folder, splitted_path)
    with open(image_path, "wb") as file:
        file.write(response.content)


def save_comments(book_id, comments, folder="comments/"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = f"{book_id}.txt"
    filepath = Path(folder, filename)

    with open(filepath, "w") as file:
        file.write(comments)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


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
    comments_soup = soup.select("#content .texts .black")
    fetched_comments = [comment.text for comment in comments_soup]
    comments = "\n".join(fetched_comments)
    genre_soup = soup.select("span.d_book a")
    genres = [genre.text for genre in genre_soup]
    parsed_page = {
        "book_name": book,
        "image_url": image_url,
        "comments": comments,
        "genres": genres,
    }

    return parsed_page


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = argparse.ArgumentParser(
        description="Script for chain downloading books from tululu.org"
    )
    parser.add_argument(
        "--start_id", "-s", type=int, help="Starting from this ID", default=1
    )
    parser.add_argument(
        "--end_id", "-e", type=int, help="Ends with this ID", default=11
    )
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id):
        try:
            parsed_page = parse_book_page(book_id)
            download_txt(book_id, parsed_page["book_name"])
            download_image(parsed_page["image_url"])
            if parsed_page["comments"]:
                save_comments(book_id, parsed_page["comments"])
        except requests.HTTPError:
            print("File URL is not valid. Skipping to next...")
            continue


if __name__ == "__main__":
    main()
