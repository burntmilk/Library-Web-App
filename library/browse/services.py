from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


# class EmptyBooksListException(Exception):
#     pass


def get_books(repo: AbstractRepository):
    books = repo.get_books()
    return books


def get_five_books(page_num: int, repo: AbstractRepository):
    books = repo.get_five_books(page_num)
    return books


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(int(book_id))
    return book


def display_book_authors(book: Book):   # String of authors separated by commas
    author_list = []
    for author in book.authors:
        author_list.append(author.full_name)
    return ", ".join(author_list)
