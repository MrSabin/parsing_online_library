import argparse
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def rebuild(books_dump):
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )
    book_cards_on_page = 20
    columns_on_page = 2
    chunked_book_cards = list(chunked(books_dump, book_cards_on_page))
    pages_count = len(chunked_book_cards)
    template = env.get_template("template.html")
    pages_folder = "pages/"
    Path(pages_folder).mkdir(parents=True, exist_ok=True)
    for page_number, chunk in enumerate(chunked_book_cards, 1):
        book_cards = list(chunked(chunk, columns_on_page))
        rendered_page = template.render(
            book_cards=book_cards,
            pages_count=pages_count,
            page_number=page_number,
        )
        filename = Path(pages_folder, f"index{page_number}.html")
        with open(filename, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(
        description="Script for science fiction books download"
    )
    parser.add_argument(
        "--json_path",
        help="Folder with JSON file",
        default="json/books_dump.json",
    )
    args = parser.parse_args()
    with open(args.json_path, "r") as file:
        books_dump = json.load(file)

    rebuild(books_dump)
    server = Server()
    server.watch("template.html", rebuild(books_dump))
    server.serve(root=".")


if __name__ == "__main__":
    main()
