import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_urls_books(args):
    url_books = []
    
    for page in range(args.start_id, args.end_id):
        url = "https://tululu.org/l55/{}".format(page)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        id_books = soup.find_all('table', class_="d_book")
        for id_book in id_books:
            id_book = id_book.find('a')['href']
            url_book = urljoin(url, id_book)
            url_books.append(url_book)

    return url_books
