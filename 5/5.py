"""
Задание №5:
1. Разработать поисковую систему на основе векторного поиска по построенному индексу.
На каждый введённый поисковый запрос выводится список документов с их “весами” отсортированный по релевантности.
Примеры запуска:
word1
word1 word2
word1 word2 word3
"""
import csv
import os
import numpy as np
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity


# Выгрузка из файлов idf, tf_idf, списка терминов и номеров документов
def load_data(tables_dir):
    idf = {}
    terms = []
    with open(os.path.join(tables_dir, 'idf_table.csv'), 'r', newline='', encoding='utf-8') as idf_file:
        reader = csv.reader(idf_file)
        for row in reader:
            if row[0] == 'Term':
                continue
            terms.append(row[0])
            idf[row[0]] = float(row[1])
    tfidf_df = pd.read_csv(os.path.join(tables_dir, 'tfidf_table.csv'))
    doc_names = tfidf_df.columns
    return idf, terms, tfidf_df, doc_names[1:]


# Создание TF-IDF векторов для файлов
def load_document_vectors(tfidf_df, docs_list):
    documents = []
    for doc in docs_list:
        documents.append(tfidf_df[str(doc)].tolist())
    return documents


def build_query_vector(query, terms, idf):
    # TF-IDF для запроса
    query_terms = query.lower().split()
    tf_idf = {term: (query_terms.count(term) / len(query_terms) * idf[term]) for term in query_terms if term in terms}
    # Вектор запроса с TF-IDF значениями
    query_vector = [tf_idf.get(term, 0) for term in terms]
    return np.array(query_vector)


def vector_search(doc_vect, query_vector, doc_names):
    # Косинусное сходство
    similarities = cosine_similarity([query_vector], doc_vect)[0]
    sorted_docs = sorted(zip(doc_names, similarities), key=lambda x: x[1], reverse=True)
    return sorted_docs


if __name__ == "__main__":
    tables_dir = "../4/tables"
    results_file = "results.json"
    # Примеры запросов
    queries = ["абсолютный", "агрессивный", "авиабилет",
               "абсолютный агрессивный", "абсолютный агрессивный авиабилет"]

    # Загрузка данных
    idf, terms, tfidf_df, doc_names = load_data(tables_dir)

    docs_vect = load_document_vectors(tfidf_df, doc_names)

    # Выполнение поиска
    search_results = {}
    for query in queries:
        query_vector = build_query_vector(query, terms, idf)
        results = vector_search(docs_vect, query_vector, doc_names)
        docs = ''
        for doc, sim in results:
            s = round(sim, 5)
            if s > 0:
                docs += f"{doc}: {s}, "
        search_results[query] = [docs]

    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(search_results, f, ensure_ascii=False, indent=4)