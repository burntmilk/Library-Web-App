from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', 'Password1')
    repo.add_user(user)
    repo.add_user(User('Martin', 'Password1'))
    user2 = repo.get_user('dave')
    print(user2)
    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('Martin', 'Password1'))
    user = repo.get_user('martin')
    assert user == User('Martin', 'Password1')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(1, 'test')
    repo.add_book(book)
    assert repo.get_book(1) == book


def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(707611)
    assert book.title == 'Superman Archives, Vol. 2'


def test_repository_can_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(-1)
    assert book is None


def test_repository_can_get_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_all_books()
    assert len(books) == 20
    assert type(books[0]) is Book


def test_repository_can_get_stock(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    stock = repo.get_book_stock(707611)
    assert stock == 0


def test_repository_can_get_price(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    price = repo.get_book_price(707611)
    assert price == 0


def test_repo_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(707611)
    review = Review(book, 'test review', 5)
    repo.add_review(review)
    assert review in repo.get_reviews()


def test_repo_cannot_add_review_with_no_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    review = Review(None, 'test review', 5)
    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repo_can_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(707611)
    assert len(repo.get_reviews()) == 0
    review = Review(book, 'test review', 5)
    repo.add_review(review)
    assert len(repo.get_reviews()) == 1


def test_repo_can_get_books_by_author_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_author_initial('a')
    assert len(books) == 2


def test_repo_can_get_empty_list_when_getting_books_by_author_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_author_initial('z')
    assert books == []


def test_repo_can_get_books_by_publisher_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_publisher_initial('a')
    assert len(books) == 4


def test_repo_can_get_empty_list_when_getting_books_by_publisher_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_publisher_initial('z')
    assert books == []


