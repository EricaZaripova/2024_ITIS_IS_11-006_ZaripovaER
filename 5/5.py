"""
Задание №5:
1. Разработать поисковую систему на основе векторного поиска по построенному индексу.
На каждый введённый поисковый запрос выводится список документов с их “весами” отсортированный по релевантности.
Примеры запуска:
word1
word1 word2
word1 word2 word3
"""
import os
import numpy as np
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity


# Чтение значений TF-IDF из файла
def load_document_vectors(tables_dir):
    documents = {}
    for file in os.listdir(tables_dir):
        doc_name = file[:-4]  # убираем '.csv'
        df = pd.read_csv(os.path.join(tables_dir, file), delimiter=',')
        documents[doc_name] = df.set_index('Term')['TF-IDF'].to_dict()
    return documents


# Вектор запроса
def build_query_vector(query, terms):
    # TF для запроса
    query_terms = query.lower().split()
    tf = {term: query_terms.count(term) / len(query_terms) for term in query_terms if term in terms}
    # Вектор запроса с TF-IDF значениями
    query_vector = [tf.get(term, 0) for term in terms]
    return np.array(query_vector)


def vector_search(documents, query_vector):
    """Find and rank documents based on cosine similarity to the query vector."""
    doc_names = list(documents.keys())
    # Массив с пока нулевыми векторами для каждого документа
    doc_vectors = np.zeros((len(documents), len(query_vector)))
    for i, doc_values in enumerate(documents.values()):
        for j, term in enumerate(terms):
            doc_vectors[i, j] = doc_values.get(term, 0)

    # Вычисляем косинусное сходство
    similarities = cosine_similarity([query_vector], doc_vectors)[0]
    sorted_docs = sorted(zip(doc_names, similarities), key=lambda x: x[1], reverse=True)
    return sorted_docs


if __name__ == "__main__":
    tables_dir = '../4/tables'
    documents = load_document_vectors(tables_dir)
    terms = {term for doc in documents.values() for term in doc}  # Получаем список всех терминов

    # Примеры запросов
    queries = ["википедия", "идентификатор аккаунт", "июль каждый как", "агентство автор аккаунт"]

    # Выполнение поиска
    search_results = {}
    for query in queries:
        query_vector = build_query_vector(query, terms)
        results = vector_search(documents, query_vector)
        docs = {}
        for doc, sim in results:
            docs[doc] = f"{sim:.5f}"
        search_results[query] = docs

    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(search_results, f, ensure_ascii=False, indent=4)
