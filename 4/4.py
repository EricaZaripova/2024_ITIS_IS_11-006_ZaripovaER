"""
Задание №4:
1. Подсчитать tf каждого термина.
2. Подсчитать idf.
3. Подсчитать tf-idf.
В выводимых таблицах округлять значение до 5-6 знаков после запятой.

Полученные параметры сохранить в виде таблиц.
"""

import os
import math
import pandas as pd


# TF: Кол-во повторений слова в доке/кол-во слов в доке
def compute_tf(document_words):
    tf = {}
    total_words = len(document_words)
    for term in document_words:
        tf[term] = tf.get(term, 0) + 1 / total_words
    return tf


# IDF: лог (Кол-во документов / на кол-во документов, где встречается слово)
def compute_idf(documents):
    idf = {}
    total_documents = len(documents)
    for document in documents:
        for term in set(document):
            idf[term] = idf.get(term, 0) + 1
    for term, count in idf.items():
        idf[term] = round(math.log(total_documents / count, 10), 6)
    return idf


def compute_tf_idf(tf, idf):
    tf_idf = {}
    for term, value in tf.items():
        tf_idf[term] = round(value * idf.get(term, 0), 6)
    return tf_idf


if __name__ == "__main__":
    tokens_dir = '../2/tokens'
    tables_dir = './tables'

    # Словарь "файл: перечень слов"
    documents = {}
    for file_name in os.listdir(tokens_dir):
        file_path = os.path.join(tokens_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            documents[file_name] = f.read().split()

    idf = compute_idf(list(documents.values()))

    # Создаем таблицы TF и TF-IDF
    tf_table = {}
    tfidf_table = {}
    for file_name, words in documents.items():
        tf = compute_tf(words)
        tf_idf = compute_tf_idf(tf, idf)

        tf_table[file_name] = tf
        tfidf_table[file_name] = tf_idf

    # Создаем таблицы pandas
    tf_df = pd.DataFrame(tf_table).fillna(0).round(6)
    tf_df.columns = [int(col[4:-4]) for col in tf_df.columns]
    tf_df = tf_df.reindex(sorted(tf_df.columns), axis=1)
    tf_df = tf_df.reindex(sorted(tf_df.index))

    tfidf_df = pd.DataFrame(tfidf_table).fillna(0).round(6)
    tfidf_df.columns = [int(col[4:-4]) for col in tfidf_df.columns]
    tfidf_df = tfidf_df.reindex(sorted(tfidf_df.columns), axis=1)
    tfidf_df = tfidf_df.reindex(sorted(tfidf_df.index))

    # Создаем таблицу IDF
    idf_df = pd.DataFrame(list(idf.items()), columns=['Term', 'IDF'])
    idf_df = idf_df.sort_values(by='Term')

    # Сохраняем таблицы в CSV
    idf_df.to_csv(os.path.join(tables_dir, 'idf_table.csv'), index=False)
    tf_df.to_csv(os.path.join(tables_dir, 'tf_table.csv'))
    tfidf_df.to_csv(os.path.join(tables_dir, 'tfidf_table.csv'))
