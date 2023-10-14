import os
import argparse
from pathlib import Path
from time import sleep

import requests
import json
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

from parse.parse_tululu_category import get_urls_books
from check_for_redirect import check_for_redirect



def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.select_one("h1")
    title_text = title_tag.text
    name, author = title_text.split(" :: ")
    book_name = name.strip()
    book_author = author.strip()

    comments = soup.select(".texts")
    comments_text = [(comment.select_one("span.black").text) for comment in comments]

    genres = soup.select_one("span.d_book").select("a")
    genres_text = [(genre.text) for genre in genres]

    img_file_path = soup.select_one("div.bookimage").select_one("img")["src"]
    img_file_path = img_file_path.replace("shots", "images")
    print(img_file_path)

    book = {
        "book_name": book_name,
        "book_author": book_author,
        "genres_text": genres_text,
        "comments_text": comments_text,
        "img_file_path": img_file_path
    }
    return book


def download_txt(url, params, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, params)
    response.raise_for_status()
    check_for_redirect(response)
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'w', encoding="utf-8") as file:
        file.write(response.text)


def download_img(url, filename, folder='/images'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    file_name = os.path.basename(urlparse(url).path)
    file_number = file_name.replace("images", "")
    new_file_name = os.path.join(folder, file_number)

    with open(new_file_name, 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(
        description='Выберите диапазон скачиваемых книг'
    )
    parser.add_argument('--start_page', help='Запуск программы с введённого числа',
                        default=1, type=int)
    parser.add_argument('--end_page', help='Конец программы с введённого числа',
                        default=10, type=int)
    parser.add_argument('--dest_folder', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON',
                        default="media", type=str)
    parser.add_argument('--skip_imgs', help='не скачивать картинки',
                        action="store_true")
    parser.add_argument('--skip_txt', help='не скачивать книги',
                        action="store_true")
    parser.add_argument('--json_path', help='указать свой путь к *.json файлу с результатами',
                        default="media", type=str)
    args = parser.parse_args()


    books_characteristics = []
    loading_book_url = "https://tululu.org/txt.php"
    books_urls = get_urls_books(args.start_page, args.end_page)
    for book_url in books_urls:
        book_number = urlparse(book_url).path.split("/")[1][1:]
        params = {"id": book_number}
        try:
            book_response = requests.get(loading_book_url, params)

            book_response.raise_for_status()
            check_for_redirect(book_response)

            page_response = requests.get(book_url)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            book = parse_book_page(page_response)
            books_characteristics.append(book)
            img_file_path =  book["img_file_path"]

            if not args.skip_imgs:
                full_img_url = urljoin(book_url, img_file_path)
                folder='images'
                path = os.path.join(args.dest_folder, folder)
                download_img(full_img_url, img_file_path, path)
            if not args.skip_txt:
                book_filename = f"{book['book_name']}.txt"
                folder='books'
                path = os.path.join(args.dest_folder, folder)
                download_txt(loading_book_url, params, book_filename, path)
        except requests.HTTPError:
            print("Такой книги нет")
        except requests.ConnectionError:
            print("Повторное подключение")
            sleep(20)
    folder = args.json_path
    os.makedirs(folder, exist_ok=True)
    filename = "book_parse.json"
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'w', encoding="utf-8") as json_file:
        json.dump(books_characteristics, json_file, ensure_ascii=False)


if __name__ == "__main__":
    main()
