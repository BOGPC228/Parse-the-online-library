import os
import argparse
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse
from parse_tululu_category import get_urls_books
import json


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id='content').find('h1')
    title_text = title_tag.text
    name, author = title_text.split(" :: ")
    book_name = name.strip()
    book_author = author.strip()

    comments = soup.find_all('div', class_="texts")
    comments_text = [(comment.find('span', class_="black").text) for comment in comments]

    genres = soup.find('span', class_="d_book").find_all('a')
    genres_text = [(genre.text) for genre in genres]

    img_file_path = soup.find('div', class_="bookimage").find('img')['src']

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


def download_img(url, filename, payload=None, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, payload)
    response.raise_for_status()
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(
        description='Выберите диапазон скачиваемых книг'
    )
    parser.add_argument('--start_id', help='Запуск программы с введённого числа',
                        default=1, type=int)
    parser.add_argument('--end_id', help='Конец программы с введённого числа',
                        default=10, type=int)
    args = parser.parse_args()
    
    books_characteristics = []
    loading_book_url = "https://tululu.org/txt.php"
    books_urls = get_urls_books()
    for book_url in books_urls:
        book_number = urlparse(book_url).path.split("/")[1][1:]
        params = {"id": book_number}
        book_response = requests.get(loading_book_url, params)
        try:
            book_response.raise_for_status()
            check_for_redirect(book_response)

            page_response = requests.get(book_url)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            book = parse_book_page(page_response)
            books_characteristics.append(book)
            img_file_path =  book["img_file_path"]

            full_img_url = urljoin(book_url, img_file_path)
            download_img(full_img_url, img_file_path)

            book_filename = f"{book['book_name']}.txt"
            download_txt(loading_book_url, params, book_filename)
        except requests.HTTPError:
            print("Такой книги нет")
        except requests.ConnectionError:
            print("Повторное подключение")
            sleep(20)
    folder = "media/"
    os.makedirs(folder, exist_ok=True)
    filename = "book_parse.json"
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'w', encoding="utf-8") as json_file:
        json.dump(books_characteristics, json_file, ensure_ascii=False)

if __name__ == "__main__":
    main()
