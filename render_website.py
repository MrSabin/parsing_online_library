import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)
with open("json/books_dump.json", "r") as file:
    books_json = file.read()
books_dump = json.loads(books_json)
books_on_page = 20
columns_on_page = 2
chunked_dump = list(chunked(books_dump, books_on_page))
pages_count = len(chunked_dump)


def rebuild():
    template = env.get_template("template.html")
    pages_folder = "pages/"
    Path(pages_folder).mkdir(parents=True, exist_ok=True)
    for page_number, chunk in enumerate(chunked_dump, 1):
        books = list(chunked(chunk, columns_on_page))
        rendered_page = template.render(
            books_dump=books,
            pages_count=pages_count,
            page_number=page_number,
        )
        filename = Path(pages_folder, f"index{page_number}.html")
        with open(filename, "w", encoding="utf8") as file:
            file.write(rendered_page)
    print("Site rebuilt")


rebuild()
server = Server()
server.watch("template.html", rebuild)
server.serve(root=".")
