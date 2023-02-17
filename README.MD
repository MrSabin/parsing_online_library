# Book parser for tululu.org online library
This script is intended for downloading books from [tululu.org](https://tululu.org) online library alongside with their covers, genre information and user`s comments.

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


## `parse_tululu_category.py` - script for download books of science fiction genre.

To run it, type
```
python3 parse_tululu_category.py
```
Optional arguments:
* `--start_page` - Download starts from that page
* `--end_page` - Download ends with that page
* `--dest_folder` - Root folder for downloaded data
* `--skip_txt` - Boolean, enables/disables books .txt download
* `--skip_images` - Boolean, enables/disables books covers download
* `--json_path` - Folder for saving books JSON dump

For example, if you want to download books from pages 15 through 25, without images, type
```python
python3 parse_tululu_category.py --start_page 15 --end_page 25 --skip_images
```

## `render_website.py` - script for render offline library website from data, gathered by `parse_tululu_category.py` script.

For example, after using `parse_tululu_category` script, type
```python
python3 render_website.py
```
Script will download all needed data, and render site pages for offline use. This script runs local server as well, you can go to `127.0.0.1:5500` and start using generated site.

You can find example of site at [GitHub Pages](https://mrsabin.github.io/parsing_online_library/)


# Project goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](dvmn.org)
