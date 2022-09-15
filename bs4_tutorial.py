import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

url = 'https://tululu.org/b1/'
response = requests.get(url)
response.raise_for_status()


soup = BeautifulSoup(response.text, 'lxml')


title_tag = soup.find(id='content').find('h1')
title_text = title_tag.text
name, author = title_text.split(" :: ")
name_book = name.strip()
author_book = author.strip()
#img_tag = soup.find('img', class_='attachment-post-image')['src']
#text_tag = soup.find('div', class_='entry-content')
#text_tags = text_tag.text
print(name_book)
print(author_book)
#print(img_tag)
#print(text_tags)
def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join(folder, sanitize_filename(filename))
    path = f"{path}.txt"
    return path

url = 'http://tululu.org/txt.php?id=1'

filepath = download_txt(url, 'Алиби')
print(filepath)  # Выведется books/Алиби.txt


filepath = download_txt(url, 'Али/би', folder='books/')
print(filepath)  # Выведется books/Алиби.txt


filepath = download_txt(url, 'Али\\би', folder='txt/')
print(filepath)  # Выведется txt/Алиби.txt

