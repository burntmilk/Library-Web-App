import abc
from typing import List
from datetime import date

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


repo_instance = None


class RepositoryException(Exception):   # Error messages for abstract repo
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_book(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self) -> List[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_stock(self, book_id: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_price(self, book_id: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.book is None:
            raise RepositoryException('No book attached to Review')

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author_initial(self, initial_letter: str) -> List[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publisher_initial(self, initial_letter: str) -> List[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_years(self) -> List[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_with_no_year(self) -> List[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_year(self, year: int) -> List[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_favourite_books(self, user_name: str) -> List[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_book_to_user_favourites(self, user_name: str, book_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_book_from_user_favourites(self, user_name, book_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def book_in_user_favourites(self, user_name: str, book_id: int) -> bool:
        raise NotImplementedError
        

