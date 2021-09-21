import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.repository import RepositoryException


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


# def test_repo_can_search_books_by_title(in_memory_repo):
#     title = "switchblade"
#     books = in_memory_repo.search_books_by_title(title)
#     assert books[0].title == "The Switchblade Mamma"
#     books = in_memory_repo.search_books_by_title("")
#     assert books != []


def test_repo_can_add_user(in_memory_repo):
    user = User('username', 'Password1')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('username') is user


def test_repo_can_get_user(in_memory_repo):
    in_memory_repo.add_user(User('username', 'Password1'))
    user = in_memory_repo.get_user('username')
    assert user == User('username', 'Password1')


def test_repo_cannot_get_invalid_user(in_memory_repo):
    user = in_memory_repo.get_user('')
    assert user is None


def test_repo_can_add_review(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    review = Review(book, "test review", 5)
    in_memory_repo.add_review(review)
    assert review in in_memory_repo.get_reviews()


def test_repo_cannot_add_review_with_no_book(in_memory_repo):
    review = Review(None, "test review", 5)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repo_can_get_reviews(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    in_memory_repo.add_review(Review(book, "test", 1))
    in_memory_repo.add_review(Review(book, "test2", 2))
    assert len(in_memory_repo.get_reviews()) == 2


