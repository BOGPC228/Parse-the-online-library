import os
import json
import math

from livereload import Server
from jinja2 import Template, Environment, FileSystemLoader
from more_itertools import chunked

def rebuild():
    with open("media/book_parse.json", 'r', encoding="utf-8") as json_file:
        books = json.load(json_file)

    books_count = len(books)
    book_pages = list(chunked(books, 20))
    count_pages = math.ceil(books_count/20)

    for page_number, page_books in enumerate(book_pages, start=1):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("template.html")
        render_html = template.render(books=page_books, 
                                      current_page=page_number,
                                      total_pages=count_pages)

        with open(F"pages/index{page_number}.html", 'w', encoding="utf-8") as html_file:
            html_file.write(render_html)
    
    print("Site rebuilt")


if __name__ == "__main__":
    os.makedirs("pages", exist_ok=True)
    
    rebuild()

    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')
