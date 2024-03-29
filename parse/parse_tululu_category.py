from time import sleep

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from check_for_redirect import check_for_redirect


def get_urls_books(start_page, end_page):
    book_urls = []
    for page in range(start_page, end_page):
        try:
            url = "https://tululu.org/l55/{}".format(page)
            response = requests.get(url)
            check_for_redirect(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            book_ids = soup.find_all('table', class_="d_book")
            for book_id in book_ids:
                book_id = book_id.find('a')['href']
                book_url = urljoin(url, book_id)
                book_urls.append(book_url)
    
            return book_urls
        except requests.HTTPError:
            print("Такой страницы нету")
        except requests.ConnectionError:
            print("Повторное подключение")
            sleep(20)