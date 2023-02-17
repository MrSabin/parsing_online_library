import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

with open("json/books_dump.json", "r") as file:
    books_json = file.read()
books_dump = json.loads(books_json)

template = env.get_template("template.html")
rendered_page = template.render(books_dump=books_dump)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
