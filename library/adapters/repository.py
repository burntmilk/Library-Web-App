import abc
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class RepositoryException(Exception):   # Error messages for abstract repo
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    pass
