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
    def get_books(self) -> List[Book]:
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
        raise NotImplementedError
