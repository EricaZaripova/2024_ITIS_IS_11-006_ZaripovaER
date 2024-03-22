"""
Задание №3:
1. Создать инвертированный список терминов (индекс) для всей коллекции документов. Отсортировать по алфавиту и сохранить его в файл.
2. Реализовать булев поиск по построенному индексу (т.е. вводится выражение содержащее слова с тремя
логическими И, ИЛИ, НЕ, по которому выдается список документов, содержащий данное выражение).
Примеры (запустить поиск с выбранным набором слов для каждого из примеров, слова должны быть одинаковыми для всех 5 примеров):
word1 & word2 | word3    word1 & !word2 | !word3
word1 | word2 | word3    word1 | !word2 | !word3
word1 & word2 & word3
"""
import os
import json


def create_inverted_index(source_dir):
    inverted_index = {}
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            words = f.read().split()
            for word in words:
                if word not in inverted_index:
                    inverted_index[word] = []
                if file_name not in inverted_index[word]:
                    inverted_index[word].append(file_name)

    # Сортировка слов в алфавитном порядке
    sorted_inverted_index = {word: sorted(files) for word, files in sorted(inverted_index.items())}
    return sorted_inverted_index


def boolean_search(query, inverted_index):
    # Поиск документов, содержащих слово (или НЕ содержащих слово)
    def resolve_query(word, invert=False):
        result = set(inverted_index.get(word, []))
        if invert:
            all_docs = {file for files in inverted_index.values() for file in files}
            return all_docs - result
        return result

    components = query.split()
    result = None
    operator = None  # хранит последнюю операцию

    for component in components:
        if component in {'&', '|'}:
            operator = component
            continue

        invert = False
        if component.startswith('!'):
            invert = True
            component = component[1:]

        if result is None:
            result = resolve_query(component, invert)
        elif operator == '&':
            result &= resolve_query(component, invert)
        elif operator == '|':
            result |= resolve_query(component, invert)

    return sorted(result) if result else []


if __name__ == "__main__":
    tokens_dir = '../2/tokens'
    inverted_index = create_inverted_index(tokens_dir)

    # Запись списка индексов в файл
    with open('inverted_index.json', 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=4)

    # Запросы для булева поиска
    queries = [
        "июль & каждый | как",
        "июль & !каждый | !как",
        "июль | каждый | как",
        "июль | !каждый | !как",
        "июль & каждый & как"
    ]

    search_results = {query: boolean_search(query, inverted_index) for query in queries}
    # Запись запросов и результатов в файл
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(search_results, f, ensure_ascii=False, indent=4)
