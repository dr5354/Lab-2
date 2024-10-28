import csv
from datetime import datetime
import random
import xml.etree.ElementTree as ET

# Чтение данных из CSV файла с указанием разделителя
def first_task(books):
    # Фильтрация строк, где длина названия больше 30 символов
    long_titles = [book for book in books if len(book['Название']) > 30]

    # Вывод количества таких строк
    print(f'Количество записей с названием длинее 30 символов: {len(long_titles)}')


def extract_year(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        return date_obj.year
    except ValueError:
        return None
def generate_bibliography(books, num_entries=20, output_file='bibliography.txt'):
    # Выбор случайных записей
    selected_entries = random.sample(books, num_entries)

    # Формирование библиографических ссылок
    bibliography = []
    for idx, row in enumerate(selected_entries):
        year = extract_year(row['Дата поступления'])
        entry = f"{row['Автор']}. {row['Название']} - {year}" if year else f"{row['Автор']}. {row['Название']} - неизвестный год"
        bibliography.append(entry)

    # Сохранение в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, entry in enumerate(bibliography, 1):
            f.write(f"{i}. {entry}\n")

    print(f'Библиографические ссылки сохранены в {output_file}')



def search_books_by_author(books, author_name, years, limit=10):
    years_set = set(years)
    author_books = [book for book in books if author_name.lower() in book['Автор'].lower() and extract_year(book['Дата поступления']) in years_set]
    return author_books[:limit]

def get_text(element, tag):
    found = element.find(tag)
    return found.text if found is not None else None

if __name__ == '__main__':
    with open('books.csv', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        books = [row for row in reader]
    first_task(books)
    author_name = 'Толстой'  # Укажите автора
    years = [2014, 2016, 2017]  # Укажите конкретные года

    print(search_books_by_author(books, author_name, years))
    generate_bibliography(books)

    tree = ET.parse('currency.xml')
    root = tree.getroot()

    currency_names = []
    for valute in root.findall('Valute'):
        nominal_text = get_text(valute, 'Nominal')
        if nominal_text is not None and int(nominal_text) == 1:
            name = get_text(valute, 'Name')
            if name is not None:
                currency_names.append(name)

    # Вывод извлеченных данных
    print("Список валют с Nominal=1:")
    for name in currency_names:
        print(name)

