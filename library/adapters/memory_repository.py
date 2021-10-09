from pathlib import Path
from typing import List     # for better documentation of function return types

from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__inventory = BooksInventory()
        self.__publishers = []
        self.__authors = []
        self.__users = []
        self.__reviews = []

    def add_book(self, book: Book):
        if self.__inventory.find_book(book.book_id) is None:    # check if already in library
            self.__inventory.add_book(book, 0, 0)   # placeholder price + stock

    def get_all_books(self) -> List[Book]:
        return self.__inventory.get_books()

    def get_book(self, book_id: int) -> Book:
        return self.__inventory.find_book(book_id)

    def get_book_stock(self, book_id: int) -> int:
        return self.__inventory.find_stock_count(book_id)

    def get_book_price(self, book_id: int) -> int:
        return self.__inventory.find_price(book_id)

    def get_user(self, user_name: str) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user_favourite_books(self, user_name: str) -> List[Book]:
        user = self.get_user(user_name)
        if user is not None:
            return user.favourite_books

    def book_in_user_favourites(self, user_name: str, book_id: int) -> bool:
        user = self.get_user(user_name)
        book = self.get_book(book_id)
        if user is not None and book is not None:
            return book in user.favourite_books

    def add_book_to_user_favourites(self, user_name: str, book_id: int):
        user = self.get_user(user_name)
        book = self.get_book(book_id)
        user.add_book_to_favourites(book)

    def remove_book_from_user_favourites(self, user_name, book_id: int):
        user = self.get_user(user_name)
        book = self.get_book(book_id)
        user.remove_book_from_favourites(book)

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self.__reviews

    def get_books_by_author_initial(self, initial_letter: str) -> List[Book]:
        books = self.get_all_books()
        author_books = []
        for book in books:
            for author in book.authors:
                if author.full_name[0].upper() == initial_letter.upper():
                    author_books.append(book)
                    break
        return author_books

    def get_books_by_publisher_initial(self, initial_letter: str) -> List[Book]:
        books = self.get_all_books()
        publisher_books = []
        for book in books:
            if book.publisher.name[0].upper() == initial_letter.upper():
                publisher_books.append(book)
        return publisher_books

    def get_book_years(self) -> List[int]:
        books = self.get_all_books()
        years = []
        for book in books:
            if book.release_year not in years and book.release_year is not None:
                years.append(book.release_year)
        return sorted(years)

    def get_books_with_no_year(self) -> List[Book]:
        books = self.get_all_books()
        no_year_books = []
        for book in books:
            if book.release_year is None:
                no_year_books.append(book)
        return no_year_books

    def get_books_by_year(self, year: int) -> List[Book]:
        books = self.get_all_books()
        books_with_year = []
        for book in books:
            if book.release_year == year:
                books_with_year.append(book)
        return books_with_year


# def load_books(data_path: Path, repo: MemoryRepository):    # makes list of book objects
#     books_filename = str(Path(data_path) / "comic_books_excerpt.json")
#     author_filename = str(Path(data_path) / "book_authors_excerpt.json")
#
#     reader = BooksJSONReader(books_filename, author_filename)
#     reader.read_json_files()
#     books_list = reader.dataset_of_books
#
#     for book in books_list:     # load the books into repo
#         repo.add_book(book)
#
#
# def load_users(data_path: Path, repo: MemoryRepository):
#     pass
#
#
# def load_reviews(data_path: Path, repo: MemoryRepository, users):
#     pass
#
#
# def populate(data_path: Path, repo: MemoryRepository):
#     load_books(data_path, repo)
