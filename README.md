# Парсим сайт с книгами

Модуль для загрузки книг и картинок с [источника](https://tululu.org/).

## Запуск

Для запуска блога у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 
```python
    pip install -r requirements.txt
```
- Для загрузки книг запустите команду и у вас скачается стандартное количество книг от 1 до 10 
```python
    python3 parse_tululu.py
```
- Для загрузки книг с возможностью выбора диапазона запустите команду 
```python
    python3 parse_tululu.py --start_id 10 --end_id 20
```
- Указать свой путь к каталогу с результатами парсинга: картинкам, книгам, JSON
```python
    python3 parse_tululu.py --dest_folder
```
- Если не хотите скачивать картинки
```python
    python3 parse_tululu.py --skip_imgs
```
- Если не хотите скачивать книги
```python
    python3 parse_tululu.py --skip_txt
```
- Указать свой путь к *.json файлу с результатами
```python
    python3 parse_tululu.py --json_path
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
