from typing import List, Iterable
from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


# class EmptyBooksListException(Exception):
#     pass


def get_books(repo: AbstractRepository):
    books = repo.get_books()
    return books


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(int(book_id))
    return book


def get_book_stock(book_id: int, repo: AbstractRepository):
    return repo.get_book_stock(book_id)


def get_book_price(book_id: int, repo: AbstractRepository):
    return repo.get_book_price(book_id)


def display_book_authors(book: Book):   # String of authors separated by commas
    author_list = []
    for author in book.authors:
        author_list.append(author.full_name)
    return ", ".join(author_list)


def get_five_books(books: List[Book], page_num: int):
    if page_num * 5 < len(books):
        return books[(page_num-1) * 5: page_num * 5]
    else:
        return books[(page_num-1) * 5: len(books)]


def get_all_books_by_id(repo: AbstractRepository):
    pass

def get_books_by_id(id_list, repo: AbstractRepository):
    # books = repo.
    pass


# ============================================
# Functions to convert model entities to dicts. model / repo data -> primitive
# ============================================

def book_to_dict(book: Book):
    book_dict = {
        'id': book.book_id,
        'title': book.title,
        'description': book.description,
        'publisher': book.publisher.name,
        'authors': book.authors,
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

