import argparse
import time
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(book_id, filename, root_folder="", folder="books/"):
    url = "https://tululu.org/txt.php"
    payload = {"id": book_id}
    sanitized_filename = sanitize_filename(filename)
    Path(root_folder, folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    book_path = Path(folder, f"{book_id}. {sanitized_filename}.txt")
    with open(book_path, "w") as file:
        file.write(response.text)

    return book_path


def download_image(image_url, root_folder="", folder="images/"):
    Path(root_folder, folder).mkdir(parents=True, exist_ok=True)
    splitted_url = urlsplit(unquote(image_url), allow_fragments=True)
    splitted_path = splitted_url.path.split("/")[-1]
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)

    image_path = Path(folder, splitted_path)
    with open(image_path, "wb") as file:
        file.write(response.content)

    return image_path


def save_comments(book_id, comments, folder="comments/"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    comments = "\n".join(comments)
    filename = f"{book_id}.txt"
    filepath = Path(folder, filename)

    with open(filepath, "w") as file:
        file.write(comments)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, "lxml")
    book_with_author = soup.find("h1").text.split("::")
    book_name, author = book_with_author
    image_partial_url = soup.find("div", class_="bookimage").find("img")["src"]
    image_url = urljoin(response.url, image_partial_url)
    comments_soup = soup.select("#content .texts .black")
    comments = [comment.text for comment in comments_soup]
    genre_soup = soup.select("span.d_book a")
    genres = [genre.text for genre in genre_soup]
    parsed_page = {
        "book_name": book_name.strip(),
        "author": author.strip(),
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
        while True:
            try:
                base_url = "https://tululu.org"
                page_url = urljoin(base_url, f"b{book_id}/")
                response = requests.get(page_url, verify=False)
                response.raise_for_status()
                check_for_redirect(response)

                parsed_page = parse_book_page(response)
                download_txt(book_id, parsed_page["book_name"])
                download_image(parsed_page["image_url"])
                if parsed_page["comments"]:
                    save_comments(book_id, parsed_page["comments"])
            except requests.HTTPError:
                print("File URL is not valid. Skipping to next...")
                continue
            except requests.ConnectionError:
                print("Connection error, retrying in 10 seconds...")
                time.sleep(10)
            finally:
                break


if __name__ == "__main__":
    main()
