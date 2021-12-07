import requests
import os
from pathlib import Path

file_path = "books"
directory = os.path.dirname(file_path)

try:
    os.stat(file_path)
except:
    os.mkdir(file_path)

for i in range(1,11):
    url = "https://tululu.org/txt.php?id=" + str(i)
    response = requests.get(url)
    response.raise_for_status() 
    filename = "books/id{}.txt".format(i)
    with open(filename, 'wb') as file:
        file.write(response.content)
