# qa_python

# Склонировал репозиторий и создал ветку develop.

# Добавил в проект файл .gitignore с исключениями для Python/pytest/VS Code, удалил из индекса __pycache__ (больше не отслеживаем).

# BooksCollector — управление коллекцией книг
Проект содержит реализацию класса `BooksCollector` и набор автотестов на базе `pytest`.

## Структура проекта
- `main.py` — класс `BooksCollector`.
- `tests.py` — автотесты (13 тестов, покрытие всех публичных методов).
- `README.md` — описание проекта.

## Реализованные тесты
В проекте реализовано 13 автотестов, покрывающих все публичные методы класса. Для повторяющихся сценариев использована параметризация (`@pytest.mark.parametrize`), что позволяет проверять несколько наборов данных без дублирования кода. Каждый тест создаёт собственный экземпляр `BooksCollector()`, обеспечивая изоляцию состояния.

# Проверка покрытия
Метод	                        Тесты
add_new_book	                1, 2, 3, 4
set_book_genre	                5, 6
get_book_genre	                7
get_books_with_specific_genre	8
get_books_genre	                12
get_books_for_children	        9
add_book_in_favorites	        10
delete_book_from_favorites	    11, 10
get_list_of_favorites_books	    13, 10, 11

Все 9 методов покрыты, параметризация в 5 тестах (2, 3, 5, 6, 8).

### Тесты для `add_new_book`
- `test_add_new_book_add_two_books` — добавление двух книг, проверка размера словаря через `get_books_genre`.
- `test_add_new_book_valid_length` (параметризованный) — успешное добавление книг с длиной названия 1 и 40 символов.
- `test_add_new_book_invalid_length` (параметризованный) — пустая строка и название из 41 символа не добавляются.
- `test_add_new_book_duplicate_not_allowed` — повторное добавление одной книги не допускается.

### Тесты для `set_book_genre` и `get_book_genre`
- `test_set_book_genre_valid` (параметризованный) — назначение допустимого жанра существующей книге, проверка через `get_book_genre`.
- `test_set_book_genre_invalid` (параметризованный) — жанр не назначается, если книги нет или жанр не из списка `genre`.
- `test_get_book_genre_empty_after_add` — у только что добавленной книги жанр равен пустой строке.

### Тест для `get_books_with_specific_genre`
- `test_get_books_with_specific_genre_there_are_matches_and_an_empty_result` (параметризованный) — возврат списка книг по жанру, включая пустой результат при отсутствии совпадений.

### Тест для `get_books_genre`
- `test_get_books_genre_returns_dict` — возвращает словарь с добавленными книгами.

### Тест для `get_books_for_children`
- `test_get_books_for_children_excludes_age_rated` — книги с жанрами из `genre_age_rating` («Ужасы», «Детективы») исключаются из списка для детей.

#### Этот тест изменён по замечанию Ревью, описание ниже!!!
    ### Тест для `add_book_in_favorites`
    - `test_add_book_in_favorites_handles_duplicates_and_safe_delete` — добавление в избранное без дублей, корректное и безопасное удаление (в том числе несуществующей книги).

### Тест для `delete_book_from_favorites`
- `test_delete_book_from_favorites_does_not_remove_from_books_dict` — при удалении из избранного книга остаётся в словаре `books_genre`.

### Тест для `get_list_of_favorites_books`
- `test_get_list_of_favorites_books_returns_list` — возвращает корректный список избранных книг.


## Требования и запуск

- Python 3.8+
- `pytest`

Запуск тестов:
pytest -v tests.py 
Ожидаемый результат: все тесты PASSED.
#### Фактический результат: 22 passed in 0.36s.

#### Замечания Ревью на тест 10 -- Нужно исправить: сценарии должны быть атомарны --
Из теста 10 делаем три атомарных теста:
- 10.1. - для `add_book_in_favorites` - "test: add atomic test for preventing duplicates in favorites"
- 10.2. - для `delete_book_from_favorites` - "test: add atomic test for removing existing book from favorites"
- 10.3. - для `delete_book_from_favorites` - "test: add atomic test for safe removal of non-existent book from favorites"
#### Замечания Ревью на тест 6 -- Нужно исправить: в тестах не должно быть условий --
#### Замечания Ревью на тест 6 -- Нужно исправить: ассерт должен быть однозначным --
- 6a
- 6b
#### Замечания Ревью на тест 10.1. -- Нужно исправить: сначала нужно проверить успешное добавление в избранное, а затем уже проектировать негативные сценарии, в том числе дубликат --
- 10.1.1.
- 10.1.2.