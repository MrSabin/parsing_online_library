import requests
from pathlib import Path

path = "books"
Path(path).mkdir(parents=True, exist_ok=True)

for book_id in range(1, 11):
    url = f"https://tululu.org/txt.php?id={book_id}"
    name = f"{book_id}.txt"

    response = requests.get(url)
    response.raise_for_status()

    filename = Path(path, name)
    with open(filename, "w") as file:
        file.write(response.text)
