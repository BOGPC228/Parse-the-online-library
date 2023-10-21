import os
import json
import math
import argparse

from livereload import Server
from jinja2 import Template, Environment, FileSystemLoader
from more_itertools import chunked


PAGES_COUNT = 20


def rebuild(json_path, PAGES_COUNT):
    with open(json_path, "r", encoding="utf-8") as json_file:
        books = json.load(json_file)

    books_count = len(books)
    pages_book = list(chunked(books, PAGES_COUNT))
    pages_count = math.ceil(books_count/PAGES_COUNT)

    for page_number, page_books in enumerate(pages_book, start=1):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("template.html")
        render_html = template.render(books=page_books, 
                                      current_page=page_number,
                                      total_pages=pages_count)

        with open(F"pages/index{page_number}.html", "w", encoding="utf-8") as html_file:
            html_file.write(render_html)
    
    print("Site rebuilt")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Пусть к Json")
    parser.add_argument("--json_path", help="указать свой путь к *.json файлу с результатами",
                        default="media/book_parse.json", type=str)
    args = parser.parse_args()

    os.makedirs("pages", exist_ok=True)

    json_path = args.json_path
    
    rebuild(json_path)

    server = Server()
    server.watch("template.html", lambda:rebuild(json_path))
    server.serve(root=".")