import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):  
    if response.history:
        raise requests.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id='content').find('h1')
    title_text = title_tag.text
    name, author = title_text.split(" :: ")
    name_book = name.strip()
    author_book = author.strip()
    filename = f"{name_book}.txt"
    return filename


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join(folder, sanitize_filename(filename))
    with open(path, 'wb') as file:
        file.write(response.content)


def main():
    for book_number in range(1,11):
        params = {"id": book_number}
        loading_book_url = "https://tululu.org/txt.php"
        book_response = requests.get(loading_book_url, params)
        page_book = f'https://tululu.org/b{book_number}/'
        try:
            book_response.raise_for_status()
            check_for_redirect(book_response)

            page_response = requests.get(page_book)
            page_response.raise_for_status()
            check_for_redirect(page_response)
            filename = parse_book_page(page_response)
            print(filename)
            download_txt(loading_book_url, filename)
        except requests.HTTPError:
            print("Такой книги нет")

    


if __name__ == "__main__":
    main()
