import pytest # Без этого параметризация (@pytest.mark.parametrize) не сработает.
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # 1. пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # !!Исправлен вызов get_books_rating → get_books_genre, так как метода get_books_rating 
        # в классе не существует!!
        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

# --- для метода add_new_book ---

    # 2. Параметризация: валидная длина (1 и 40 символов)
    @pytest.mark.parametrize("name", ["А", "Б" * 40])
    def test_add_new_book_valid_length(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    # 3. Параметризация: невалидная длина (пустая строка, 41 символ)
    @pytest.mark.parametrize("name", ["", "В" * 41])
    def test_add_new_book_invalid_length(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    # 4. Запрет дубликатов
    def test_add_new_book_duplicate_not_allowed(self):
        collector = BooksCollector()
        collector.add_new_book("Дубликат")
        collector.add_new_book("Дубликат")
        assert len(collector.get_books_genre()) == 1

# --- для метода set_book_genre ---

    # 5. Параметризация: установка валидного жанра
    @pytest.mark.parametrize("name, genre", [("КнигаА", "Фантастика"), ("КнигаБ", "Комедии")])
    def test_set_book_genre_valid(self, name, genre):
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    # 6a. Книга не добавлена — жанр не устанавливается
    def test_set_book_genre_book_not_added_genre_not_set(self):
        collector = BooksCollector()
        collector.set_book_genre("Несуществующая", "Фантастика")
        assert collector.get_book_genre("Несуществующая") is None

# --- для метода get_book_genre ---

    # 7. У новой книги жанр — пустая строка
    def test_get_book_genre_empty_after_add(self):
        collector = BooksCollector()
        collector.add_new_book("БезЖанра")
        assert collector.get_book_genre("БезЖанра") == ""

# --- для метода get_books_with_specific_genre ---

    # 8. Параметризация: получение книг по жанру (есть совпадения и пустой результат)
    @pytest.mark.parametrize("genre, expected", [
        ("Фантастика", ["Книга1", "Книга2"]),
        ("Ужасы", []),
    ])
    def test_get_books_with_specific_genre(self, genre, expected):
        collector = BooksCollector()
        for name in ["Книга1", "Книга2"]:
            collector.add_new_book(name)
            collector.set_book_genre(name, "Фантастика")
        assert collector.get_books_with_specific_genre(genre) == expected

# --- для метода get_books_for_children ---

    # 9. Фильтрация «для детей»: исключение возрастных жанров
    def test_get_books_for_children_excludes_age_rated(self):
        collector = BooksCollector()
        # Книги для детей
        collector.add_new_book("Мультик")
        collector.set_book_genre("Мультик", "Мультфильмы")
        # Возрастные жанры
        collector.add_new_book("Страшный")
        collector.set_book_genre("Страшный", "Ужасы")
        children = collector.get_books_for_children()
        assert "Мультик" in children
        assert "Страшный" not in children

# --- для метода add_book_in_favorites ---

    # 10.1. Добавление в избранное: запрет дублей
    def test_add_book_in_favorites_prevents_duplicates(self):
        collector = BooksCollector()
        name = "Любимая"
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        collector.add_book_in_favorites(name)  # повторный вызов
        assert collector.get_list_of_favorites_books() == [name]

# --- для метода delete_book_from_favorites ---

    # 10.2. Удаление из избранного: успешное удаление
    def test_delete_book_from_favorites_removes_existing_book(self):
        collector = BooksCollector()
        name = "Любимая"
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        collector.delete_book_from_favorites(name)
        assert collector.get_list_of_favorites_books() == []

    # 10.3. Удаление из избранного: безопасное удаление несуществующей книги
    def test_delete_book_from_favorites_does_nothing_if_not_present(self):
        collector = BooksCollector()
        # Книга не добавлялась в избранное вообще
        collector.delete_book_from_favorites("НетВИзбранном")
        assert collector.get_list_of_favorites_books() == []

    # 11. Проверка, что книга остаётся в словаре после удаления из избранного
    def test_delete_book_from_favorites_does_not_remove_from_books_dict(self):
        collector = BooksCollector()
        name = "Остаётся"
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        collector.delete_book_from_favorites(name)
        # Книга должна остаться в словаре, но уйти из избранного
        assert name in collector.get_books_genre()
        assert name not in collector.get_list_of_favorites_books()

# --- для метода get_books_genre ---

    # 12. возврат словаря с книгами
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book("КнигаX")
        collector.add_new_book("КнигаY")
        result = collector.get_books_genre()
        assert isinstance(result, dict)
        assert "КнигаX" in result
        assert "КнигаY" in result

# --- для метода get_list_of_favorites_books ---

    # 13. возврат списка избранных книг
    def test_get_list_of_favorites_books_returns_list(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        result = collector.get_list_of_favorites_books()
        assert isinstance(result, list)
        assert len(result) == 2
        assert "Книга1" in result
        assert "Книга2" in result