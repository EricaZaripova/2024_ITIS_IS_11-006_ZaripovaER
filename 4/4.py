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
        idf[term] = math.log(total_documents / count)
    return idf


def compute_tf_idf(tf, idf):
    tf_idf = {}
    for term, value in tf.items():
        tf_idf[term] = value * idf.get(term, 0)
    return tf_idf


if __name__ == "__main__":
    tokens_dir = '../2/tokens'
    tables_dir = 'tables'

    # Формируем словари формата "файл: массив со словами"
    documents = {}
    for file_name in os.listdir(tokens_dir):
        file_path = os.path.join(tokens_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            documents[file_name] = f.read().split()

    idf = compute_idf(list(documents.values()))

    for file_name, words in documents.items():
        tf = compute_tf(words)
        tf_idf = compute_tf_idf(tf, idf)

        # Записываем TF, IDF, TF-IDF в табличные файлы
        df = pd.DataFrame(list(zip(tf.keys(), tf.values(), idf.values(), tf_idf.values())),
                          columns=['Term', 'TF', 'IDF', 'TF-IDF'])
        df = df.round(6)
        df.sort_values(by='Term', inplace=True)

        csv_file_name = file_name.replace('.txt', '.csv')
        csv_path = os.path.join(tables_dir, csv_file_name)
        df.to_csv(csv_path, index=False, sep=',')
