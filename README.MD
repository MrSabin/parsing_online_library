# Book parser for tululu.org online library
This script is intended for downloading books from tululu.org online library alongside with their covers, genre information and user`s comments.

## Installation

Python 3 should be already installed.
Install dependencies by running
```python
pip install -r requirements.txt
```

## Running

Run the `main.py` script by typing
```python
python3 main.py --start_id "id" --end_id "id"
```
or
```python
python3 main.py -s "id" -e "id"
```
where `--start_id` or `-s` for short - starting page, and `--end_id` or `-e` for short - ending page.

For example, if you type
```python
python3 main.py -s 1 -e 20
```
script will download books from page 1 to page 20. If no arguments inputed at all, default indexes will be used, which from 1 to 10 page.

Script will make directories for downloaded content inside current working directory - `books` for books .txt files, `images` for books covers and `comments` for book user comments, saved in .txt file.
