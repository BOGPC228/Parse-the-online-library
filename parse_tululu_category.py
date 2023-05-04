import requests
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parse_tululu import check_for_redirect


def get_urls_books(args):
    books_url = []
    try:
        for page in range(args.start_page, args.end_page):
            url = "https://tululu.org/l55/{}".format(page)
            response = requests.get(url)
            check_for_redirect(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            books_id = soup.find_all('table', class_="d_book")
            for book_id in books_id:
                book_id = book_id.find('a')['href']
                book_url = urljoin(url, book_id)
                books_url.append(book_url)

        return books_url
    except requests.HTTPError:
        print("Такой страницы нету")
    except requests.ConnectionError:
        print("Повторное подключение")
        sleep(20)