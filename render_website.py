import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)
with open("json/books_dump.json", "r") as file:
    books_json = file.read()
books_dump = json.loads(books_json)
chunked_dump = list(chunked(books_dump, 2))


def rebuild():
    template = env.get_template("template.html")
    rendered_page = template.render(books_dump=chunked_dump)
    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)
    print("Site rebuilt")


rebuild()
server = Server()
server.watch("template.html", rebuild)
server.serve(root=".")
