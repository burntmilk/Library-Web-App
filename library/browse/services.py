from typing import List, Iterable
from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class NonExistentBookException(Exception):
    pass


def get_book(book_id: int, repo: AbstractRepository) -> dict:
    book = repo.get_book(int(book_id))
    if book is None:
        raise NonExistentBookException
    return book_to_dict(book)


def get_all_books(repo: AbstractRepository) -> List[Book]:
    books = repo.get_books()
    books_dto = []
    if len(books) > 0:
        books_dto = books_to_dict(books)
    return books_dto


def get_book_stock(book_id: int, repo: AbstractRepository) -> int:
    stock = repo.get_book_stock(book_id)
    if stock is None:
        raise NonExistentBookException
    return stock


def get_book_price(book_id: int, repo: AbstractRepository) -> int:
    price = repo.get_book_price(book_id)
    if price is None:
        raise NonExistentBookException
    return price


# ============================================
# Functions to convert model entities to dicts. model / repo data -> primitive
# ============================================

def book_to_dict(book: Book):
    book_dict = {
        'book_id': book.book_id,
        'title': book.title,
        'description': book.description,
        'publisher': book.publisher.name,
        'authors': authors_to_dict(book.authors),
        'release_year': book.release_year,
        'ebook': book.ebook,
        'num_pages': book.num_pages
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):  # returns list of books in dict format
    return [book_to_dict(book) for book in books]


def author_to_dict(author: Author):
    author_dict = {
        'author_id': author.unique_id,
        'full_name': author.full_name
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]

