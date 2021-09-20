import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


def test_repo_can_add_book(in_memory_repo):
    book = Book(12345, "test book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(12345) is book


def test_repo_can_retrieve_book(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    assert book.title == "The Switchblade Mamma"
    assert in_memory_repo.get_book_price(book.book_id) == 0


def test_repo_can_get_all_books(in_memory_repo):
    books = in_memory_repo.get_books()
    assert len(books) == 20


def test_repo_can_search_books_by_title(in_memory_repo):
    title = "switchblade"
    books = in_memory_repo.search_books_by_title(title)
    assert books[0].title == "The Switchblade Mamma"
    books = in_memory_repo.search_books_by_title("")
    assert books != []
