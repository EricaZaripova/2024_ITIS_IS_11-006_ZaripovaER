"""
Задание №2:
1. Из сохраненных документов выделить отдельные слова (токенизация).
2. Лемматизировать токены (допускается использование сторонних библиотек).
3. Отбросить стоп-слова.
4. Сохранить отдельно обработанные документы.
Русский язык обязателен.
"""

import os
import pymorphy2
from nltk.corpus import stopwords


russian_stopwords = set(stopwords.words('russian'))
morph = pymorphy2.MorphAnalyzer()


# Удаление стоп-слов из параграфа и приведение слов к нормальной форме
def process_paragraph(paragraph):
    tokens = paragraph.split()
    tokens = [token for token in tokens
              if token and
              token not in russian_stopwords and
              3 <= len(token) < 20]
    lemmatized_tokens = [morph.parse(token)[0].normal_form for token in tokens]
    return ' '.join(lemmatized_tokens)



def process_text_files(pages_dir, tokens_dir):
    if not os.path.exists(tokens_dir):
        os.makedirs(tokens_dir)

    for file_name in os.listdir(pages_dir):
        if file_name.endswith('.txt'):
            page_path = os.path.join(pages_dir, file_name)
            token_path = os.path.join(tokens_dir, file_name)

            # Обработка текста
            with open(page_path, 'r', encoding='utf-8') as f:
                paragraphs = f.read().split('\n')  # разделение по параграфам
                processed_paragraphs = [process_paragraph(paragraph) for paragraph in paragraphs]
                processed_text = '\n'.join(processed_paragraphs)

            # Сохранение текста
            with open(token_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)


if __name__ == "__main__":
    pages_dir = '../1/pages'
    tokens_dir = 'tokens'

    process_text_files(pages_dir, tokens_dir)

