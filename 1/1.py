"""
Задание №1:
1. Скачать минимум 100 текстовых страниц с помощью краулера.
2. Записать каждую страницу (без html-кода) в отдельный текстовый файл.
3. Создать файл index.txt, в котором хранится номер документа и ссылка на страницу.
Входным аргументом программы должны быть веб-адреса нескольких страниц.
Ссылки с первой страницы ведут на другие, которые также скачиваются и заносятся в файл index.txt.
Если на первой странице не набралось достаточного количества страниц (100), то операция повторяется для дочерних страниц первой.
Каждая страница должна содержать не менее 1000 слов.
"""
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re


# Проверка количества слов в тексте
def word_count(text):
    words = text.split()
    return len(words)


# Скачивание страниц
def download_pages(start_urls, max_pages=100, min_words=1000):
    crawled_urls = set()
    to_crawl = set(start_urls)
    index = []  # номер страницы и URL
    page_count = 0

    while to_crawl and page_count < max_pages:
        current_url = to_crawl.pop()
        if current_url not in crawled_urls:
            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.text, features="html.parser")
                # Удаление скриптов и стилей
                for script_or_style in soup(["script", "style"]):
                    script_or_style.decompose()
                # Деление на абзацы
                paragraphs = soup.get_text().split('\n')
                clean_texts = []
                for p in paragraphs:
                    # Оставляем только слова на русском
                    russian_text = re.findall(r'\b[а-яёА-ЯЁ]+\b', p)
                    clean_text = ' '.join(russian_text)
                    if clean_text:
                        clean_texts.append(clean_text)

                # Объединяем абзацы и проверяем общее количество слов
                full_text = '\n'.join(clean_texts)
                if word_count(full_text) >= min_words:
                    crawled_urls.add(current_url)
                    page_count += 1
                    file_name = f'doc_{page_count}.txt'
                    file_path = os.path.join(documents_dir, file_name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(full_text)
                    index.append(f'{page_count}: {current_url}')
                    # Поиск новых ссылок
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if (href and
                                not href.startswith('http') and
                                not ('#' in href or
                                     href.endswith('.svg') or
                                     href.endswith('.png') or
                                     href.endswith('.jpg') or
                                     href.endswith('.jpeg') or
                                     href.endswith('.webp'))):
                            href = urljoin(current_url, href)
                        to_crawl.add(href)
            except requests.exceptions.RequestException:
                continue

    with open('index.txt', 'w', encoding='utf-8') as f:
        for entry in index:
            f.write(entry + '\n')


if __name__ == "__main__":
    documents_dir = 'pages'
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

    start_urls = ['https://ru.wikipedia.org/wiki/Python']
    download_pages(start_urls)


