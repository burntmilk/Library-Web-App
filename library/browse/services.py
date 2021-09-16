from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


# class EmptyBooksListException(Exception):
#     pass


def get_books(repo: AbstractRepository):
    books = repo.get_books()
    # if not books:   # list empty
    #     raise EmptyBooksListException
    return books
