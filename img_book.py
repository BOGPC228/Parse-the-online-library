from fileinput import filename
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


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

    commends = soup.find_all('div', class_="texts")
    text_commends = []
    for commend in commends:
        text_commends.append(commend.find('span', class_="black").text)
    
    genres = soup.find('span', class_="d_book").find_all('a')
    text_genres = []
    for genre in genres:
        text_genres.append(genre.text)

    filename_img = soup.find('div', class_="bookimage").find('img')['src']
    filename_book = f"{name_book}.txt"
    return filename_book, filename_img


def download_txt(url, params, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, params)
    response.raise_for_status()
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
    book_img_url = "https://tululu.org/"
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

            filename_book, filename_img = parse_book_page(page_response)
            full_img_url = urljoin(book_img_url, filename_img)
            download_img(full_img_url, filename_img)
            
            download_txt(loading_book_url, params, filename_book)
        except requests.HTTPError:
            print("Такой книги нет")


if __name__ == "__main__":
    main()
